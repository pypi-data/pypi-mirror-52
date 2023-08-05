import flask
import hashlib
import importlib
import marshmallow
import marshmallow.fields
import os
import logging
import types

from bert import constants, binding, utils, exceptions, remote_exceptions, remote_utils, remote_callback

from urllib.parse import urlparse

from werkzeug.exceptions import NotFound
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

logger = logging.getLogger()

SENTRY_DSN: str = os.environ.get('SENTRY_DSN', None)
if SENTRY_DSN:
    logger.info('Sentry DSN Enabled')
    import sentry_sdk
    sentry_sdk.init(SENTRY_DSN)

APP: flask.Flask = flask.Flask(f'{constants.SERVICE_NAME}-webservice')
APP.secret_key = constants.WWW_SECRET
APP.debug = constants.DEBUG
MIDDLEWARE: DispatcherMiddleware = DispatcherMiddleware(NotFound(), {
  '': APP,
})
MIDDLEWARE.secret_key = constants.WWW_SECRET
MIDDLEWARE.debug = constants.DEBUG
JOBS: [str, types.FunctionType] = {}

def load_service_module(service_module: str) -> '__module__':
  try:
    module = importlib.import_module(f'{constants.SERVICE_MODULE}.jobs')
  except ImportError:
    raise NotImplementedError(f'Unable to find Service Module[{constants.SERVICE_MODULE}]. Is it in PythonPath?')

  for member_name in dir(module):
    if member_name.startswith('_'):
      continue

    member = getattr(module, member_name)
    if type(member) != types.FunctionType:
      continue

    if hasattr(member, 'func_space'):
      JOBS[member_name] = member

def setup_service() -> DispatcherMiddleware:
  if constants.SERVICE_NAME == None:
    raise NotImplementedError('Missing ENVVar[SERVICE_NAME]')

  if constants.SERVICE_HOST == None:
    raise NotImplementedError(f'Missing ENVVar[SERVICE_HOST]')

  job_chain: typing.List[types.FunctionType] = binding.build_job_chain()
  noop_queue: utils.Queue = utils.Queue(binding.NOOP_SPACE)

  entry_point: types.FunctionType = job_chain[0]
  if entry_point.schema is None:
    raise exceptions.SchemaRequired

  # Error Handling
  @APP.errorhandler(remote_exceptions.BadRequest)
  def _handle_bad_request(exception: remote_exceptions.BadRequest) -> flask.Response:
    if isinstance(exception, remote_exceptions.BadRequest):
      return exception.as_response()

    raise exception

  route_name__queue: str = f'/{constants.SERVICE_NAME}.queue'
  @APP.route(route_name__queue, methods=['POST'])
  def entry_point_handler() -> flask.Response:
    config: remote_utils.RemoteConfig = remote_utils.RemoteConfig.Obtain()
    if flask.request.headers.get('Authorization', None) != f'Bearer {config.auth_token}':
      raise remote_exceptions.BadRequest('Unauthorized', {}, 403)

    data: remote_utils.PostData = remote_utils.PostData.Obtain(schema=entry_point.schema)
    noop_queue.put(data.data)
    return flask.Response('{}', content_type='application/json', status=200)

  class ShakeSchema(marshmallow.Schema):
    auth_token: str = marshmallow.fields.String(required=True)
    queue_url: str = marshmallow.fields.String(required=True)
    shake_url: str = marshmallow.fields.String(required=True)
    callback_url: str = marshmallow.fields.String(required=True)

  route_name__shake: str = f'/{constants.SERVICE_NAME}.shake'
  @APP.route(route_name__shake, methods=['POST'])
  def entry_point__shake() -> flask.Response:
    config: remote_utils.RemoteConfig = remote_utils.RemoteConfig.Obtain()
    if flask.request.headers.get('Authorization', None) != f'Bearer {config.nonce}':
      raise remote_exceptions.BadRequest('Unauthorized', {}, 403)

    if flask.request.headers.get('Authorization', 'noop') == 'Bearer noop':
      raise remote_exceptions.BadRequest('Unauthorized', {}, 403)

    data = remote_utils.PostData.Obtain(schema=ShakeSchema)
    service_parts = urlparse(constants.SERVICE_HOST)
    shake_parts = urlparse(data.data['shake_url'])
    if shake_parts.path != route_name__shake or shake_parts.netloc != service_parts.netloc:
      raise NotImplementedError

    queue_parts = urlparse(data.data['queue_url'])
    if queue_parts.path != route_name__queue or shake_parts.netloc != service_parts.netloc:
      raise NotImplementedError

    remote_utils.RemoteConfig.Update({
      'nonce': 'noop',
      'auth_token': data.data['auth_token'],
      'callback_url': data.data['callback_url']
    })

    return flask.Response('{}', content_type='application/json', status=200)

  return MIDDLEWARE


def run_service() -> DispatcherMiddleware:
  run_simple('0.0.0.0', constants.WWW_PORT, MIDDLEWARE, use_reloader=False)


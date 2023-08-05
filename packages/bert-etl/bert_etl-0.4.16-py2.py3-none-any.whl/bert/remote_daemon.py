import json
import logging
import os
import requests
import time

from bert import remote_utils, constants, binding, utils, remote_callback

STARTUP_DELAY: float = 1.0
DELAY: float = .1
STOP_DAEMON: bool = False
logger = logging.getLogger(__name__)

SENTRY_DSN: str = os.environ.get('SENTRY_DSN', None)
if SENTRY_DSN:
    logger.info('Sentry DSN Enabled')
    import sentry_sdk
    sentry_sdk.init(SENTRY_DSN)

def handle_signal(sig, frame):
  if sig == 2:
    global STOP_DAEMON
    STOP_DAEMON = True
    import sys; sys.exit(0)

  else:
    logger.info(f'Unhandled Signal[{sig}]')

def setup_service() -> None:
  if constants.SERVICE_NAME == None:
    raise NotImplementedError('Missing ENVVar[SERVICE_NAME]')

  if constants.MAIN_SERVICE_NONCE is None:
    raise NotImplementedError(f'Missing ENVVar[MAIN_SERVICE_NONCE]')

  if constants.MAIN_SERVICE_HOST is None:
    raise NotImplementedError(f'Missing ENVVar[MAIN_SERVICE_HOST]')

  remote_utils.RemoteConfig.Update({'nonce': constants.MAIN_SERVICE_NONCE})
  for retry_attempt in range(0, 10):
    url: str = f'{constants.MAIN_SERVICE_HOST}/{constants.SERVICE_NAME}.register'
    response = requests.post(url, data=json.dumps({'nonce': constants.MAIN_SERVICE_NONCE}), headers={
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    })
    if not response.status_code in [200]:
      logger.exception({
        'url': url,
        'contents': response.json()
      })
      logger.info(f'Retrying in {STARTUP_DELAY} seconds')
      time.sleep(STARTUP_DELAY)

    else:
      break

  else:
    response.raise_for_status()


def run_service():
  if not constants.DEBUG:
    raise NotImplementedError

  if constants.DEBUG:
    job_chain: typing.List[types.FunctionType] = binding.build_job_chain()
    noop_queue: utils.Queue = utils.Queue(binding.NOOP_SPACE)
    job_queue: utils.Queue = utils.Queue(job_chain[0].work_key)

    while STOP_DAEMON is False:
      try:
        details: typing.Dict[str, typing.Any] = next(noop_queue)
      except StopIteration:
        time.sleep(DELAY)

      else:
        job_queue.put(details)

        for job in job_chain:
          logger.info(f'Running Job[{job.func_space}] as [{job.pipeline_type.value}] for [{job.__name__}]')
          job()

        else:
          tail_queue: utils.Queue = utils.Queue(job.done_key)
          for details in tail_queue:
            remote_callback.submit(constants.SERVICE_NAME, details)


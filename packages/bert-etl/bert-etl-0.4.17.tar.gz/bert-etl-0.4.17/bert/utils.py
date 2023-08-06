#!/usr/env/bin python

import boto3
import collections
import copy
import logging
import hashlib
import importlib
import json
import multiprocessing
import os
import redis
import shutil
import subprocess
import time
import typing
import types

import requests

from datetime import datetime

from bert import constants, datasource, encoders as bert_encoders

from urllib.parse import urlparse, ParseResult

logger = logging.getLogger(__name__)
PWN = typing.TypeVar('PWN')

class QueuePacker(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.strftime(constants.DATETIME_FORMAT)

    return super(QueuePacker, self).default(obj)

class Across:
  '''
  Sometimes checking to see if something exists arcoss processes is required to complete a job. Knowing where it exists is faster than searching for where it might exist in space.
  '''

  def __init__(self) -> None:
    self._conn: datasource.RedisConnection = datasource.RedisConnection.ParseURL(constants.REDIS_URL)

  def __enter__(self, redis_key: str) -> PWN:
    self._key = redis_key
    return self

  def __exit__(self, type, value, tb) -> PWN:
    self._key = None
    return self

  def exists(self) -> bool:
    value: typing.Any = self._conn.client.get(self._key)
    if value:
      return True

    return False

class DynamodbQueue:
    DEFAULT_DELAY: int = 1728000
    @staticmethod
    def Pack(datum: typing.Dict[str, typing.Any]) -> str:
        """
        Dict -> AWS Dict -> json.dumps
        """
        datum = bert_encoders.encode_object(datum)
        return datum

    @staticmethod
    def UnPack(datum: str) -> typing.Dict[str, typing.Any]:
        """
        AWS Dynamodb Dict -> Dict
        """
        return bert_encoders.decode_object(datum)

    _key: str = None
    def __init__(self: PWN, key: str) -> None:
        self._key = key

    def __iter__(self) -> PWN:
        return self

    def __next__(self) -> typing.Any:
        value = self.get()
        if value is None or value == 'STOP':
            raise StopIteration

        return value

    def put(self: PWN, value: typing.Dict[str, typing.Any]) -> None:
        combined: str = ''.join(sorted(bert_encoders.encode_identity_object(value)))
        identity: str = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        value: str = self.__class__.Pack({'identity': identity, 'datum': copy.deepcopy(value)})
        client: typing.Any = boto3.client('dynamodb')
        client.put_item(TableName=self._key, Item=value)

    def get(self: PWN) -> typing.Dict[str, typing.Any]:
        client: typing.Any = boto3.client('dynamodb')
        try:
            value: typing.Any = client.scan(TableName=self._key, Select='ALL_ATTRIBUTES', Limit=1)['Items'][0]
        except IndexError:
            return None

        else:
            unpacked: typing.Dict[str, typing.Any] = self.__class__.UnPack(copy.deepcopy(value)['datum'])
            client.delete_item(TableName=self._key, Key={'identity': value['identity']})
            return unpacked

class StreamingQueue(DynamodbQueue):
    """
    When deploying functions to AWS Lambda, auto-invocation is available as an option to run the functions. With StreamingQueue, we want to push local objects into
        the available API already utilized. We also want to keep the available `put` function so that the `done_queue` api will still push contents into the next `work_queue`.
        We'll also argment the local `get` function api and only pull from records local to the stream and not pull from dynamodb.
    """
    _key: str = None
    # Share the memory across invocations, within the same process/thread. This allows for
    #   comm_binders to be called multipule-times and still pull from the same queue
    _queue: typing.List[typing.Dict[str, typing.Any]] = []
    def __init__(self: PWN, key: str) -> None:
        self._key = key

    def local_put(self: PWN, record: typing.Dict[str, typing.Any]) -> None:
        print('Putting Record')
        # print(json.dumps(record))
        self._queue.append(copy.deepcopy(record))
        print('queue len', id(self), len(self._queue))

    def get(self: PWN) -> typing.Dict[str, typing.Any]:
        print('Getting Record')
        print('queue len', id(self), len(self._queue))
        try:
            value: typing.Any = self._queue.pop(0)
        except IndexError:
            return None

        else:
            print('value')
            print(value)
            unpacked: typing.Dict[str, typing.Any] = self.__class__.UnPack(value['datum'])
            print(unpacked)
            client = boto3.client('dynamodb')
            client.delete_item(TableName=self._key, Key={'identity': value['identity']})
            return unpacked

class LocalQueue(DynamodbQueue):
    """
    When testing, its convenient to use only a LocalQueue
    """
    _key: str = None
    # Share the memory across invocations, within the same process/thread. This allows for
    #   comm_binders to be called multipule-times and still pull from the same queue
    _queue: typing.List[typing.Dict[str, typing.Any]] = []
    def __init__(self: PWN, key: str) -> None:
        self._key = key

    def local_put(self: PWN, record: typing.Dict[str, typing.Any]) -> None:
        self._queue.append(copy.deepcopy(record))

    def put(self: PWN, record: typing.Dict[str, typing.Any]) -> None:
        logger.info(f'LocalQueue Put[{record}]')

    def get(self: PWN) -> typing.Dict[str, typing.Any]:
        try:
            value: typing.Any = self._queue.pop(0)
        except IndexError:
            return None

        else:
            return value

class Queue:
  DEFAULT_DELAY: int = 1728000
  @staticmethod
  def Pack(datum: typing.Dict[str, typing.Any]) -> str:
    return json.dumps(datum, cls=QueuePacker)

  @staticmethod
  def UnPack(datum: str) -> typing.Dict[str, typing.Any]:
    return json.loads(datum)

  def __init__(self, redis_key: str):
    self._key = redis_key
    self._redis_client = datasource.RedisConnection.ParseURL(constants.REDIS_URL).client

  def __iter__(self):
    return self

  def __next__(self):
    value = self.get()
    if value is None or value == 'STOP':
      raise StopIteration

    return value

  def peg(self, key: str, delay: str=DEFAULT_DELAY) -> bool:
    value: str = self._redis_client.get(key)
    if value is None:
      self._redis_client.set(key, 1)
      self._redis_client.expire(key, delay)
      return True

    return False

  def flushdb(self) -> None:
    self._redis_client.flushdb()

  def put_block(self, value: str, delay: int=1728000) -> None:
    value_sorted = ''.join(sorted(value))
    value_sorted = ''.join(['put-block', value_sorted])
    value_hash = hashlib.md5(value_sorted.encode('utf-8')).hexdigest()
    if self._redis_client.get(value_hash) is None:
      self._redis_client.set(value_hash, 1)
      self._redis_client.expire(value_hash, delay)
      self.put(value)

  def size(self) -> int:
    return int(self._redis_client.llen(self._key))

  def get(self) -> typing.Dict[str, typing.Any]:
    try:
      value: str = self._redis_client.lpop(self._key).decode('utf-8')
    except AttributeError:
      return 'STOP'

    else:
      return self.__class__.UnPack(value)

  def put(self, value: typing.Dict[str, typing.Any]) -> None:
    value: str = self.__class__.Pack(value)

    self._redis_client.rpush(self._key, value.encode('utf-8'))

  def bulk(self, stop_iter_key: str, bulk_count: int=50000) -> typing.List[str]:

    index: int = 0
    datums: typing.List[str] = []
    while index < bulk_count:
      datum: str = self._redis_client.lpop(self._key)
      if datum is None:
        break

      if datum == stop_iter_key:
        break

      datums.append(datum.decode('utf-8'))

    logging.info(len(datums))
    return datums

def scan_jobs(options) -> typing.Dict[str, typing.Any]:
    jobs: typing.Dict[str, typing.Any] = {}
    module = importlib.import_module(f'{options.module_name}.jobs')
    for member_name in dir(module):
        if member_name.startswith('_'):
            continue

        member = getattr(module, member_name)
        if type(member) != types.FunctionType:
            continue

        if not hasattr(member, 'done_key') or not hasattr(member, 'work_key'):
            continue

        jobs[member_name] = member

    # Order the jobs correctly
    ordered = collections.OrderedDict()
    while len(ordered.keys()) != len(jobs.keys()):
        if len(ordered.keys()) == 0:
            for job_name, job in jobs.items():
                if job.parent_func == 'noop':
                    ordered[job_name] = job
                    break

            else:
                raise NotImplementedError(f'NoopSpace not found')

        else:
            latest: types.FunctionType = [item for item in ordered.values()][-1]
            for job_name, job in jobs.items():
                if job.parent_func == latest:
                    ordered[job_name] = job
                    break
    return ordered

def find_in_elem(elem, *args) -> str:
  base = elem
  for key in args:
    try:
      base = base.find(fix_tag(key))
    except Exception as err:
      return 0

  else:
    if base == None:
      return 0

    elif base.text == None:
      return 0

    elif isinstance(base.text, bytes):
      return base.text.decode('utf-8')

    elif isinstance(base.text, str):
      return base.text

    else:
      import ipdb; ipdb.set_trace()
      return 0

def parse_timestamp(input_datetime: str) -> datetime:
  if input_datetime == 0:
    return None

  return datetime.strptime(input_datetime, '%Y-%m-%dT%H:%M:%SZ')

def fix_schema_tag(tag) -> str:
  return '{http://www.w3.org/2001/XMLSchema}%s' % tag

def fix_tag(tag) -> str:
  return '{http://www.mediawiki.org/xml/export-0.10/}%s' % tag

def zero_file(filepath, file_size):
  with open(filepath, 'wb') as stream:
    for chunk in iter(lambda: b'\0' * 4096, b''):
      stream.write(chunk)
      if stream.tell() > file_size:
        break

def run_command(cmd: str, allow_error: typing.List[int] = [0]) -> str:
  ologger = logging.getLogger('.'.join([__name__, multiprocessing.current_process().name]))
  cmd: typing.List[str] = cmd.split(' ')
  proc = subprocess.Popen(' '.join(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  while proc.poll() is None:
    time.sleep(.1)

  if proc.poll() > 0:
    if not proc.poll() in allow_error:
      raise NotImplementedError(f'{proc.poll()}, {proc.stderr.read()}')

    return proc.stderr.read().decode(constants.ENCODING)

  return proc.stdout.read().decode('utf-8')

def comm_binders(func: types.FunctionType) -> typing.Tuple[Queue, Queue, 'ologger']:
    logger.info(f'Bert Queue Type[{constants.QueueType}]')
    ologger = logging.getLogger('.'.join([func.__name__, multiprocessing.current_process().name]))
    if constants.QueueType is constants.QueueTypes.Dynamodb:
        return DynamodbQueue(func.work_key), DynamodbQueue(func.done_key), ologger

    elif constants.QueueType is constants.QueueTypes.StreamingQueue:
        return StreamingQueue(func.work_key), StreamingQueue(func.done_key), ologger

    elif constants.QueueType is constants.QueueTypes.LocalQueue:
        return LocalQueue(func.work_key), LocalQueue(func.done_key), ologger

    elif constants.QueueType is constants.QueueTypes.Redis:
        return Queue(func.work_key), Queue(func.done_key), ologger

    else:
        raise NotImplementedError(constants.QueueType)

def new_module(options: typing.Any) -> None:
  import bert
  operating_dir: str = os.path.join(os.getcwd(), options.new_module)
  if not os.path.exists(operating_dir):
    os.makedirs(operating_dir)

  bert_jobs_filepath: str = os.path.join(os.path.dirname(bert.__file__), 'jobs.py')
  jobs_file: str = os.path.join(operating_dir, 'jobs.py')
  if not os.path.exists(jobs_file):
    shutil.copyfile(bert_jobs_filepath, jobs_file)

  logger.info(f'''
  Run the new module with the following command:
  bert-runner.py -j sync_sounds -m {options.new_module}
  ''')

def show_how(options: typing.Any) -> None:
  logger.info('''
  Run the new module with the following command:
  bert-runner.py -j <job_name> -m <module_name>
  ''')


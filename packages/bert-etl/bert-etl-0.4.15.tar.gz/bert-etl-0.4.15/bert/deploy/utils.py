import boto3
import collections
import glob
import logging
import inspect
import json
import os
import shutil
import tempfile
import time
import types
import typing
import zipfile

from bert.deploy import shortcuts as bert_deploy_shortcuts

from botocore.errorfactory import ClientError

# Related: https://github.com/Miserlou/Zappa/pull/56
# Related: https://github.com/Miserlou/Zappa/pull/581
ZIP_EXCLUDES: typing.List[str] = [
    '*.exe', '*.DS_Store', '*.Python', '*.git', '.git/*', '*.zip', '*.tar.gz',
    '*.hg', 'pip', 'docutils*', 'setuputils*', '__pycache__/*',
]
COMMON_EXCLUDES: typing.List[str] = ['env', 'lambdas']

logger = logging.getLogger(__name__)

def _calc_lambda_name(lambda_name: str) -> str:
    return lambda_name

def _calc_table_name(lambda_key: str) -> str:
    return lambda_key

def copytree(src: str, dest: str, metadata: bool = True, symlinks: bool = False, ignore: typing.Any = None) -> None:
    if not os.path.exists(dest):
        os.makedirs(dest)
        if metadata:
            shutil.copystat(src, dest)

    dir_list: typing.List[str] = os.listdir(src)
    if ignore:
        excl = ignore(src, dir_list)
        dir_list = [item for item in dir_list if item not in excl]

    for item in dir_list:
        source_path: str = os.path.join(src, item)
        dest_path: str = os.path.join(dest, item)
        if symlinks and os.path.islink(source_path):
            if os.path.lexsits(dest_path):
                os.remove(dest_path)

            os.symlink(os.readlink(source_path), dest_path)
            if metadata:
                try:
                    stats: typing.Any = os.lstat(source_path)
                    mode = stat.S_IMODE(stats.st_mode)
                    os.lchmod(dest_path, mode)
                except:
                    pass # lchmod not availabe

        elif os.path.isdir(source_path):
            copytree(source_path, dest_path, metadata, symlinks, ignore)

        else:
            shutil.copy2(source_path, dest_path) if metadata else shutil.copy(source_path, dest_path)

def find_site_packages_dir(start: str, find: str) -> str:
    """
    Scan a directory[start] for a subdirectory[find]
    """
    if not os.path.isdir(start):
        raise IOError(f'Path[{start}] is not a directory.')

    for root, dirs, files in os.walk(start):
        if find in dirs:
            return os.path.join(start, find)

        for dir_name in dirs:
            result: str = find_site_packages_dir(os.path.join(start, dir_name), find)
            if result:
                return result

def get_current_venv(excludes: typing.List[str] = []):
    if not 'VIRTUAL_ENV' in os.environ.keys():
        return None

    venv = os.environ['VIRTUAL_ENV']
    # egg_links: typing.List[str] = []
    temp_package_path: str = tempfile.mkdtemp(prefix='bert-etl-packages')
    site_package_dir: str = find_site_packages_dir(venv, 'site-packages')
    # egg_links.extend(glob.glob(os.path.join(site_package_dir, '*.egg-link')))

    excludes = ZIP_EXCLUDES + excludes + ['lamdbas']
    logger.info(f'Creating Site-Packages Path[{temp_package_path}]')
    copytree(site_package_dir, temp_package_path, metadata=False, symlinks=False, ignore=shutil.ignore_patterns(*excludes))
    return temp_package_path

def get_pyenv_venv():
    if not os.path.exists('.python-version'):
        return None

def get_conda_venv(excludes: typing.List[str] = []):
    from distutils.sysconfig import get_python_lib
    python_lib: str = get_python_lib()
    if 'conda/envs' in python_lib or 'miniconda/envs' in python_lib:
        temp_package_path: str = tempfile.mkdtemp(prefix='bert-etl-packages')
        excludes = ZIP_EXCLUDES + excludes + ['lamdbas']
        logger.info(f'Creating Site-Packages Path[{temp_package_path}]')
        copytree(python_lib, temp_package_path, metadata=False, symlinks=False, ignore=shutil.ignore_patterns(*excludes))
        return temp_package_path

def build_project_envs(jobs: typing.Dict[str, types.FunctionType], venv_path: str, excludes: typing.List[str] = COMMON_EXCLUDES) -> typing.Dict[str, typing.Any]:
    confs: typing.Dict[str, typing.Any] = {}
    bert_configuration = bert_deploy_shortcuts.load_local_configuration()

    for job_name, job in jobs.items():
        env_vars: typing.Dict[str, str] = bert_deploy_shortcuts.merge_env_vars(
            bert_configuration.get('every_lambda', {'environment': {}})['environment'],
            bert_configuration.get(job_name, {'environment': {}})['environment'])
        env_vars['QUEUE_TYPE'] = env_vars.get('QUEUE_TYPE', 'dynamodb')
        runtime: str = bert_configuration.get('runtime', 'python3.6')
        try:
            memory_size: str = int(bert_configuration.get('memory_size', '512'))
        except ValueError:
            raise NotImplementedError('MemorySize must be an integer')

        project_path: str = tempfile.mkdtemp(prefix=f'bert-etl-project-{job_name}')
        logger.info(f'Creating Project Path[{project_path}]')
        job_templates: str = ''.join([f"""def {jn}():
    pass
""" for jn in jobs.keys() if jn != job_name])

        job_follow: str = inspect.getsource(job).split('\n')[0]
        job_source: str = '\n'.join(inspect.getsource(job).split('\n')[2:])
        job_template: str = """
%s
import typing
from bert import utils, constants, binding, shortcuts
%s
def %s(event, context=None):

    records: typing.List[typing.Dict[str, typing.Any]] = event.get('Records', [])
    if len(records) > 0:
        constants.QueueType = constants.QueueTypes.StreamingQueue
        work_queue, done_queue, ologger = utils.comm_binders(%s)
        for record in records:
            if record['eventName'].lower() == 'INSERT'.lower():
                work_queue.local_put(record['dynamodb']['NewImage'])

    else:
        work_queue, done_queue, ologger = utils.comm_binders(%s)

%s
    return {}
""" % (job_templates, job_follow, job_name, job_name, job_name, job_source)
        job_path: str = os.path.join(project_path, f'{job_name}.py')

        with open(job_path, 'w') as stream:
            stream.write(job_template)

        logger.info(f'Creating Job[{job_name}] Project')
        copytree(os.getcwd(), project_path, metadata=False, symlinks=False, ignore=shutil.ignore_patterns(*excludes))
        logger.info(f'Merging Job[{job_name}] Site Packages')
        copytree(venv_path, project_path, metadata=False, symlinks=False, ignore=shutil.ignore_patterns(*excludes))
        confs[_calc_lambda_name(job_name)] = {
                'project-path': project_path,
                'table-name': f'{job_name}-stream',
                # 'runtime': 'python3.7',
                'runtime': runtime,
                'memory-size': memory_size, # must be a multiple of 64, increasing memory size also increases cpu allocation
                'environment': env_vars,
                'handler-name': f'{job_name}.{job_name}',
                'spaces': {
                    'work-key': job.work_key,
                    'done-key': job.done_key,
                    'pipeline-type': job.pipeline_type,
                    'workers': job.workers,
                    'scheme': job.schema,
                }
            }

    return confs

def build_package(job_name: str, job_conf: typing.Dict[str, typing.Any], excludes: typing.List[str] = COMMON_EXCLUDES) -> None:
    try:
        compression_method: int = zipfile.ZIP_DEFLATED
    except ImportError: #pragma: no cover
        compression_method: int = zipfile.ZIP_STORED

    archive_name: str = f'{job_name}.zip'
    archive_dir: str = os.path.join(os.getcwd(), 'lambdas')
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    archive_path: str = os.path.join(archive_dir, archive_name)
    logger.info(f'Building Lambda[{job_name}] Archive[{archive_path}]')

    job_conf['archive-path'] = archive_path
    with zipfile.ZipFile(archive_path, 'w', compression_method) as archive:
        for root, dirs, files in os.walk(job_conf['project-path']):
            for filename in files:
                if filename in excludes:
                    continue

                if filename.endswith('.pyc'):
                    continue

                abs_filename: str = os.path.join(root, filename)
                if filename.endswith('.py'):
                    os.chmod(abs_filename, 0o755)

                zip_info: zipfile.ZipInfo = zipfile.ZipInfo(os.path.join(root.replace(job_conf['project-path'], '').lstrip(os.sep), filename))
                zip_info.create_system = 3
                zip_info.external_attr = 0o755 << int(16)
                with open(abs_filename, 'rb') as file_stream:
                    archive.writestr(zip_info, file_stream.read(), compression_method)

            for dirname in dirs:
                if dirname in excludes:
                    continue


    job_conf['archive-path'] = archive_path

def build_lambda_archives(jobs: typing.Dict[str, types.FunctionType]) -> str:
    venv_path: str = get_current_venv()
    if venv_path is None:
        venv_path = get_pyenv_venv()
        if venv_path is None:
            venv_path = get_conda_venv()
            if venv_path is None:
                raise NotImplementedError

    archive_paths: typing.List[str] = []
    lambdas: typing.Dict[str, typing.Any] = collections.OrderedDict()
    for job_name, job_conf in build_project_envs(jobs, venv_path).items():
        build_package(job_name, job_conf)
        lambdas[job_name] = job_conf
        # shutil.rmtree(venv_path)
        shutil.rmtree(job_conf['project-path'])

    return lambdas

def destroy_dynamodb_tables(jobs: typing.Dict[str, typing.Any]) -> None:
    table: typing.Any = None
    client = boto3.client('dynamodb')
    for job_name, job in jobs.items():
        work_table_name: str = _calc_table_name(job.work_key)
        done_table_name: str = _calc_table_name(job.done_key)

        try:
            client.delete_table(TableName=work_table_name)
        except ClientError as err:
            pass

        else:
            logger.info(f'Destorying Table[{work_table_name}]')

        try:
            client.delete_table(TableName=done_table_name)
        except ClientError as err:
            pass

        else:
            logger.info(f'Destorying Table[{done_table_name}]')


def build_dynamodb_tables(lambdas: typing.Dict[str, typing.Any]) -> None:
    table: typing.Any = None
    client = boto3.client('dynamodb')
    for lambda_name, conf in lambdas.items():
        work_table_name: str = _calc_table_name(conf['spaces']['work-key'])
        done_table_name: str = _calc_table_name(conf["spaces"]["done-key"])

        try:
            conf['work-table'] = client.describe_table(TableName=work_table_name)
        except ClientError as err:
            logger.info(f'Creating Dynamodb Table[{work_table_name}]')
            client.create_table(
                    TableName=work_table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'identity',
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'identity',
                            'AttributeType': 'S'
                        }
                    ],
                    StreamSpecification={
                        'StreamEnabled': True,
                        'StreamViewType': 'NEW_IMAGE'
                    },
                    BillingMode='PAY_PER_REQUEST')
            conf['work-table'] = client.describe_table(TableName=work_table_name)

        try:
            conf['done-table'] = client.describe_table(TableName=done_table_name)
        except ClientError as err:
            logger.info(f'Creating Dynamodb Table[{done_table_name}]')
            client.create_table(
                    TableName=done_table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'identity',
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'identity',
                            'AttributeType': 'S'
                        }
                    ],
                    StreamSpecification={
                        'StreamEnabled': True,
                        'StreamViewType': 'NEW_IMAGE'
                    },
                    BillingMode='PAY_PER_REQUEST')

            conf['done-table'] = client.describe_table(TableName=done_table_name)


def create_lambda_roles(lambdas: typing.Dict[str, typing.Any]) -> None:
    trust_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "apigateway.amazonaws.com",
                        "lambda.amazonaws.com",
                        "events.amazonaws.com",
                        "dynamodb.amazonaws.com",
                    ]
                },
                "Action": "sts:AssumeRole",
            }
        ]
    }

    policy_document: typing.Dict[str, typing.Any] = {
        "Version": "2012-10-17",
        "Statement": [
            # {
            #     "Effect": "Allow",
            #     "Action": [
            #         "xray:PutTraceSegments",
            #         "xray:PutTelemetryRecords",
            #     ],
            #     "Resource": ["*"],
            # },
            # {
            #     "Effect": "Allow",
            #     "Action": [
            #         "lambda:InvokeFunction"
            #     ],
            #     "Resource": ["*"],
            # },
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:*",
                ],
                "Resource": "arn:aws:dynamodb:*:*:table/*",
            },
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:CreateLogGroup",
                ],
                "Resource": "arn:aws:logs:*:*:*",
            }
        ]
    }
    trust_policy_name: str = 'bert-etl-lambda-execution-policy-trust'
    policy_name: str = 'bert-etl-lambda-execution-policy'
    iam_role = {
        'Path': '/',
        'RoleName': trust_policy_name,
        'AssumeRolePolicyDocument': json.dumps(trust_policy_document),
        'Description': 'Bert-ETL Lambda Execution Role',
    }
    iam_policy = {
        'Path': '/',
        'PolicyName': policy_name,
        'PolicyDocument': json.dumps(policy_document),
        'Description': 'Bert-ETL Lambda Execution Policy'
    }
    iam_client = boto3.client('iam')
    role = bert_deploy_shortcuts.map_iam_role(trust_policy_name)
    if role is None:
        iam_client.create_role(**iam_role)
        role = bert_deploy_shortcuts.map_iam_role(trust_policy_name)

    policy = bert_deploy_shortcuts.map_iam_policy(policy_name)
    if policy is None:
        iam_client.create_policy(**iam_policy)
        policy = bert_deploy_shortcuts.map_iam_policy(policy_name)
        iam_client.attach_role_policy(RoleName=trust_policy_name, PolicyArn=policy['Arn'])

    for job_name, conf in lambdas.items():
        conf['iam-role'] = role
        conf['iam-policy'] = policy

def destory_lambda_to_table_bindings(lambdas: typing.Dict[str, typing.Any]) -> None:
    client = boto3.client('lambda')
    for lambda_name, conf in lambdas.items():
        for event_mapping in client.list_event_source_mappings(
                EventSourceArn=conf['work-table']['Table']['LatestStreamArn'],
                FunctionName=lambda_name)['EventSourceMappings']:
            client.delete_event_source_mapping(UUID=event_mapping['UUID'])

def destroy_lambdas(jobs: typing.Dict[str, typing.Any]) -> None:
    client = boto3.client('lambda')
    for job_name, job in jobs.items():
        lambda_name: str = _calc_lambda_name(job_name)
        try:
            client.delete_function(FunctionName=lambda_name)
        except ClientError as err:
            pass

        else:
            logger.info(f'Deleting function[{lambda_name}]')


def upload_lambdas(lambdas: typing.Dict[str, typing.Any]) -> None:
    client = boto3.client('lambda')
    for lambda_name, conf in lambdas.items():
        try:
            client.get_function(FunctionName=lambda_name)['Configuration']
        except ClientError as err:
            logger.info(f'Creating AWSLambda for Job[{lambda_name}]')
            lambda_description = client.create_function(
                FunctionName=lambda_name,
                Runtime=conf['runtime'],
                MemorySize=conf['memory-size'],
                Role=conf['iam-role']['Arn'],
                Handler=conf['handler-name'],
                Code={
                    'ZipFile': open(conf['archive-path'], 'rb').read(),
                },
                Timeout=900,
                Environment={'Variables': conf['environment']},
            )
            conf['aws-lambda'] = client.get_function(FunctionName=lambda_name)['Configuration']

        else:
            logger.info(f'Replacing AWSLambda for Job[{lambda_name}]')
            client.delete_function(FunctionName=lambda_name)
            client.create_function(
                FunctionName=lambda_name,
                Runtime=conf['runtime'],
                MemorySize=conf['memory-size'],
                Role=conf['iam-role']['Arn'],
                Handler=conf['handler-name'],
                Code={
                    'ZipFile': open(conf['archive-path'], 'rb').read(),
                },
                Timeout=900,
                Environment={'Variables': conf['environment']},
            )
            conf['aws-lambda'] = client.get_function(FunctionName=lambda_name)['Configuration']

def bind_lambdas_to_tables(lambdas: typing.Dict[str, typing.Any]) -> None:
    client = boto3.client('lambda')
    for lambda_name, conf in lambdas.items():
        logger.info(f'Mapping Lambda[{lambda_name}] to Work-Table')
        client.create_event_source_mapping(
                EventSourceArn=conf['work-table']['Table']['LatestStreamArn'],
                FunctionName=lambda_name,
                Enabled=True,
                StartingPosition='LATEST')


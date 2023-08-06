import base64
import bcrypt
import boto3
import datetime
import os
import time
import typing

from botocore.exceptions import ClientError
from decimal import Decimal
from itertools import groupby

from .click_helpers import unimportant, fake_progress

Status = typing.NamedTuple(
  'Status', 
  [
    ('in_progress', bool), 
    ('failed', bool),
  ]
)

s3 = boto3.client('s3')
cf = boto3.client('cloudformation')

def parse_status(status):
  all_statuses = [
    'CREATE_IN_PROGRESS'
    'CREATE_FAILED'
    'CREATE_COMPLETE'
    'ROLLBACK_IN_PROGRESS'
    'ROLLBACK_FAILED'
    'ROLLBACK_COMPLETE'
    'DELETE_IN_PROGRESS'
    'DELETE_FAILED'
    'DELETE_COMPLETE'
    'UPDATE_IN_PROGRESS'
    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS'
    'UPDATE_COMPLETE'
    'UPDATE_ROLLBACK_IN_PROGRESS'
    'UPDATE_ROLLBACK_FAILED'
    'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS'
    'UPDATE_ROLLBACK_COMPLETE'
    'REVIEW_IN_PROGRESS'
  ]
  return Status(
    status.endswith('_IN_PROGRESS'),
    'ROLLBACK_' in status or status.endswith('_FAILED'),
  )

def download(config, url):
  if url.startswith('s3://'):
    bucket, _, key = url[5:].partition('/')
  else:
    bucket = config.get("source_bucket", 'nf-batch-runner')
    key = url
  return s3.get_object(Bucket=bucket, Key=key)

def create_stack(environment, template, frontend, version, ami=None):
  session_secret = base64.b64encode(os.urandom(256//8)).decode('utf8')
  now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  params = dict(
    StackName=environment,
    TemplateBody=template,
    Parameters=[
        {
            'ParameterKey': 'DeployFrontend',
            'ParameterValue': 'yes' if frontend else 'no',
        },
        {
            'ParameterKey': 'SessionSecret',
            'ParameterValue': session_secret,
        },
        {
          'ParameterKey': 'FrontendStaticPrefix',
          'ParameterValue': f"/frontend/{version}",
        }
    ],
    TimeoutInMinutes=60,
    Capabilities=[
        'CAPABILITY_NAMED_IAM',
    ],
    OnFailure='DELETE',
    Tags=[
        {
            'Key': 'nf-batch-runner',
            'Value': environment
        },
        {
            'Key': 'nf-batch-runner-version',
            'Value': version
        },
    ]
  )
  if ami is not None:
    params['Parameters'].append(
      {
          'ParameterKey': 'WorkerNodeAMI',
          'ParameterValue': ami,
      }
    )
  response = cf.create_stack(**params)
  return response['StackId']

def wait_for_resource(stack, resource):
  while True:
    try:
      response = cf.describe_stack_resource(
        StackName=stack,
        LogicalResourceId=resource
      )
    except ClientError as e:
      time.sleep(5)
      continue
    raw_status = response['StackResourceDetail']['ResourceStatus']
    status = parse_status(raw_status)
    if status.failed:
      return response['StackResourceDetail']['PhysicalResourceId'], False, response['StackResourceDetail']['ResourceStatusReason']
    if status.in_progress:
      time.sleep(5)
      continue
    return response['StackResourceDetail']['PhysicalResourceId'], True, "Complete"

MINUTES = 60

def wait_for_stack(stack):
  expected_runtime = 20 * MINUTES
  progress_half_life = 5 * MINUTES
  unimportant("It can take 15-20 minutes to create your envionment")
  with fake_progress(expected_runtime, progress_half_life) as tick:
    while True:
      tick()
      try:
        response = cf.describe_stacks(StackName=stack)
      except ClientError as e:
        time.sleep(5)
        continue
      stack_details = response['Stacks'][0]
      raw_status = stack_details['StackStatus']
      status = parse_status(raw_status)
      if status.failed:
        outputs = {}
        break
      if status.in_progress:
        time.sleep(5)
        continue
      outputs = stack_details['Outputs']
      outputs = { o['OutputKey']: o['OutputValue'] for o in outputs }
      break
  return outputs

def list_bucket_contents(bucket, prefix, ContinuationToken=None):
  params = dict(
    Bucket=bucket,
    MaxKeys=100,
    Prefix=prefix
  )
  if ContinuationToken:
    params['ContinuationToken'] = ContinuationToken
  resp = s3.list_objects_v2(**params)
  yield from resp.get('Contents', [])
  if resp['IsTruncated']:
    yield from list_bucket_contents(bucket, prefix, resp['NextContinuationToken'])

def sync(from_, to):
  from_bucket, _, from_prefix = from_[5:].partition('/')
  to_bucket, _, to_prefix = to[5:].partition('/')

  for obj in list_bucket_contents(from_bucket, from_prefix):
    from_key = obj['Key']
    to_key = from_key.replace(from_prefix, to_prefix)
    unimportant(f"s3://{from_bucket}/{from_key} -> s3://{to_bucket}/{to_key}", nl=False)
    s3.copy_object(
      ACL='private',
      Bucket=to_bucket,
      CacheControl='max-age=0',
      CopySource={'Bucket': from_bucket, 'Key': from_key},
      Key=to_key,
      StorageClass='STANDARD'
    )
    unimportant(" ✓")

def create_user(users_db, user, password=None, credits=100):
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(users_db)

  record = {
    "configs": [],
    "credits": {
      "balance": credits,
      "lastDebited": int(time.time()),
      "maxBalance": credits,
      "rate": Decimal(credits) / (28 * 24 * 60 * 60)
    },
    "metadata": {},
    "user": user
  }
  
  if password:
    record['password'] = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(14)).decode('utf8')

  table.put_item(
    Item=record,
    ReturnValues='NONE',
    ReturnConsumedCapacity='NONE',
    ReturnItemCollectionMetrics='NONE'
  )

def create_batches(objects, count):
  for _, batch in groupby(enumerate(objects), lambda el: el[0] // count):
    yield (el for _, el in batch)

def delete_objects(bucket, prefix):
  objects = list_bucket_contents(bucket, prefix)
  count = 0
  for batch in create_batches(objects, 1000):
    batch_objects = [ { 'Key': obj['Key'] } for obj in batch ]
    s3.delete_objects(
      Bucket=bucket,
      Delete={
          'Objects': batch_objects,
          'Quiet': True
      }
    )
    count += len(batch_objects)
  return count
    
def delete_bucket(bucket):
  try:
    n_objects = delete_objects(bucket, "")
    s3.delete_bucket(Bucket=bucket)
    return n_objects
  except s3.exceptions.NoSuchBucket:
    return 0
  
def delete_stack(stack):
  cf.delete_stack(
    StackName=stack,
  )

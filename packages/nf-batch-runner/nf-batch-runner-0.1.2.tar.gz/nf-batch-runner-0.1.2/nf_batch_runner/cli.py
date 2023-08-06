import boto3
import click
import os
import time
import yaml

from botocore.exceptions import NoCredentialsError
from os.path import join, expanduser

from .click_helpers import info, unimportant, panic, error

def read_config(ctx):
  ctx.obj['config'].seek(0)
  config = yaml.safe_load(ctx.obj['config'])
  config = {} if config is None else config
  return config

def write_config(ctx, config):
  ctx.obj['config'].seek(0)
  ctx.obj['config'].truncate(0)
  yaml.dump(config, ctx.obj['config'])

@click.group()
@click.option('-c', '--config', type=click.File(mode='a+'), default=expanduser(join("~", ".nf-batch-runner")))
@click.option('--region', default=None)
@click.pass_context
def cli(ctx, config, region):
  """
  Run Nextflow in AWS Batch

  Helps you to setup and manage Nextflow environments in AWS Batch
  """

  ctx.ensure_object(dict)
  ctx.obj['config'] = config

  try:
    sts = boto3.client("sts")
    ctx.obj['account_details'] = sts.get_caller_identity()
  except NoCredentialsError:
    panic("No AWS credentials found")

  config = read_config(ctx)
  if config.get('region') and region:
    panic(f"Region is already set in {config.name}, no need to set it again")
  elif not region:
    region = "eu-west-2"
  elif config.get('region'):
    region = config.get('region')

  boto3.setup_default_session(region_name=region)
 
  ctx.obj['region'] = region
  
@cli.command()
@click.option('--yes', '-y', default=False, is_flag=True)
@click.pass_context
def delete(ctx, yes):
  """Delete your enviroment"""
  from .aws import delete_bucket, delete_stack
  config = read_config(ctx)
  
  environment = config['environment']
  stack = config['stack_id']
  
  if not yes:
    click.confirm(f"Are you sure you want to delete the environment '{environment}'", abort=True)

  outputs = config.get("outputs", {})
  try:
    files_bucket = outputs["FilesBucket"]
  except KeyError:
    pass
  else:
    if not yes:
      delete_files = click.confirm(f"Do you want to delete the files in {files_bucket}")
    else:
      delete_files = True

    if delete_files:
      n_objects = delete_bucket(files_bucket)
      unimportant(f"Deleted {n_objects} objects from {files_bucket}")

  try:
    frontend_bucket = outputs["FrontendBucket"]
  except KeyError:
    pass
  else:
    delete_bucket(frontend_bucket)
    unimportant(f"Deleted {frontend_bucket}")

  delete_stack(stack)
  info(f"Deleted {environment}")

  config_path = ctx.obj['config'].name
  os.rename(config_path, f"{config_path}.{int(time.time())}.backup")

@cli.command()
def user():
  """Add, remove, update users of the frontend"""
  # Ask for a name
  # Ask for a password
  # Lookup the UsersDb
  # Add or update the User
  raise NotImplementedError()

@cli.command()
@click.option('--yes', '-y', default=False, is_flag=True)
@click.option('--ami', default=None, type=str)
@click.argument('environment', default='')
@click.pass_context
def create(ctx, yes, ami, environment):
  """Create your enviroment"""
  from .environment import pick_password, pick_environment, lookup_version, fetch_template, pick_ami
  from .aws import create_stack, wait_for_resource, wait_for_stack, sync, create_user

  config = read_config(ctx)
  config['region'] = ctx.obj['region']

  if ami is not None:
    config['AMI'] = ami
  elif config['region'] != 'eu-west-2':
    error("We currently only have an AMI built for eu-west-2 (London).  You may be able to use this tool in other regions if you build your own AMI")
    config['AMI'] = pick_ami()

  if config.get('environment'):
    panic(f"You already have an environment called {config.get('environment')}")
  config['environment'] = pick_environment(environment)
  password = pick_password()

  account_details = ctx.obj['account_details']
  if not yes:
    click.confirm(f"Are you happy to install nf-batch-runner in account {account_details['Account']}", abort=True)
    if not click.confirm(f"Does you user ({account_details['Arn'].partition('/')[-1]}) have administrator privileges"):
      panic("It is unlikely that we could create all the required resources, aborting")
    frontend = click.confirm("Do you want to deploy the web interface", default=True)
  else:
    frontend = True
  config['version'] = lookup_version(config)

  template = fetch_template(config, config['version'])

  config['stack_id'] = create_stack(config['environment'], template, frontend, config['version']['version'], config.get('AMI'))

  write_config(ctx, config)
  if frontend:
    unimportant("Waiting for the S3 bucket for the frontend (takes around a minute)", nl=False)
    bucket_name, ok, message = wait_for_resource(config['stack_id'], 'FrontendBucket')
    if not ok:
      error(" ✗")
      error("There was a problem creating the bucket")
      panic(message)
    unimportant(" ✓")
    sync(config['version']['frontend'], f"s3://{bucket_name}/frontend/{config['version']['version']}/")

  unimportant("Waiting for the users database (takes around a minute)", nl=False)
  users_db, ok, message = wait_for_resource(config['stack_id'], 'UsersDb')
  if not ok:
    error(" ✗")
    error("There was a problem creating the users database")
    panic(message)
  unimportant(" ✓")
  
  unimportant("Creating the users in the database", nl=False)
  create_user(users_db, "__GLOBAL", credits=1000)
  create_user(users_db, "admin", password, credits=100)
  unimportant(" ✓")

  outputs = wait_for_stack(config['stack_id'])
  config['outputs'] = outputs

  if frontend:
    info(f"Visit https://{outputs['FrontendUrl']} and login with the user 'admin'")
  else:
    info(f"Your environment is not ready")
  info(f"You can upload your files here: https://s3.console.aws.amazon.com/s3/buckets/{outputs['FilesBucket']}/")

  write_config(ctx, config)

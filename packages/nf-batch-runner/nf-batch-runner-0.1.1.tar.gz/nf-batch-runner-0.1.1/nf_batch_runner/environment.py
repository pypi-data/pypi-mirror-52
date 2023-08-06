import boto3
import click
import json
import re

from botocore.exceptions import ClientError

from .click_helpers import panic, error, unimportant

def pick_environment(environment, attempts=3):
  if attempts <= 0:
    panic("Giving up")
  elif environment == '':
    click.echo("What do you want to call your environment?")
    environment = click.prompt("Environment")
  elif not re.match("^[a-zA-Z][a-zA-Z0-9\-]*$", environment):
    error("Environment must start with a letter and only contain letters numbers and '-'")
    environment = click.prompt("Environment")
  elif len(environment) > 128:
    error("Environment must be less than 128 characters")
    environment = click.prompt("Environment")
  else:
    try:
      cf = boto3.client('cloudformation')
      cf.describe_stacks(StackName=environment)
    except ClientError:
      # stack doesn't exist
      return environment
    else:
      error("Environment with that name already exists")
      environment = click.prompt("Environment")
  return pick_environment(environment, attempts-1)

def pick_password(attempts=3):
  click.echo("Please give us a password you will use to login to the frontend")
  password = click.prompt("Password", default=None, hide_input=True)
  if password != click.prompt("Repeat", default=None, hide_input=True):
    error("Those passwords don't match")
    if attempts <= 0:
      panic("Giving up")
    return pick_password(attempts-1)
  return password

def pick_ami(attempts=3):
  click.echo("Which AMI would you like to use?")
  ami = click.prompt("AMI ID")
  if not ami:
    if attempts <= 0:
      panic("Giving up")
    return pick_ami(attempts-1)
  return ami

def lookup_version(config):
  from .aws import download

  unimportant("Fetching the latest version", nl=False)
  if config.get('version'):
    unimportant(f" ({config['version']['version']}) [from config]")
    return config['version']
  versions = json.load(download(config, 'versions.json')['Body'])
  unimportant(f" ({versions['latest']['version']})")
  return versions['latest']

def fetch_template(config, version):
  from .aws import download

  unimportant("Downloading the infrastructure template", nl=False)
  template = download(config, version['backend'])['Body'].read()
  unimportant(" ✓")
  return template.decode('utf8')
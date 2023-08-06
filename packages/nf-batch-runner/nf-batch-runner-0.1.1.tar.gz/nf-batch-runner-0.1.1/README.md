# nf-batch-runner

nf-batch-runner is a tool which makes it easier to run Nextflow pipelines in your AWS account.

*This tool is not endorsed by Nextflow or AWS*

Using AWS Batch, you can run pipelines in the cloud which scale up and down quickly so that 
you don't pay for servers to sit idle.

## How it works

nf-batch-runner pulls down an AWS CloudFormation template and deploys it into your AWS account.  This
creates resources which are needed to run a Nextflow pipeline in AWS.

It also creates an optional web frontend so that you can starts pipelines from your web browser.

You can [find out more](https://gitlab.com/cgps/nf-batch-runner) in our README.

## Usage

Create an AWS account and create credentials for an Admin user.  It may be posssible to run this tool
with lower priviledges but it needs to create IAM resources so it won't help a lot.

Setup your default credentials as if you were going to [use the AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

This tool has been tested running from OSX and Windows machines with Python 3.  Linux is probably also fine.

```
$ pip install nf-batch-runner
$ nf-batch-runner create my-environment
Please give us a password you will use to login to the frontend
Password:
Repeat:
Are you happy to install nf-batch-runner in account 012345678910 [y/N]: y
Does you user (ben) have administrator priviledges [y/N]: y
Do you want to deploy the web interface [Y/n]:
Fetching the latest version (v0.0.1)
Downloading the infrastructure template ✓
Waiting for the S3 bucket for the frontend (takes around a minute) ✓
...
Waiting for the users database (takes around a minute) ✓
Creating the users in the database ✓
It can take 15-20 minutes to create your envionment
  [###############---------------------]   42%  00:12:51
Visit https://d1q83rcyz9fxwf.cloudfront.net and login with the user 'admin'
You can upload your files here: https://s3.console.aws.amazon.com/s3/buckets/bt5-cli-test-filesbucket-4t1whgy2vc16/
```

You will be asked to create a password for the web interface and to confirm that you're happy for us to proceed.

After 15-20 minute the command will complete and it will give you a URL to log into the frontend and
a URL to upload files for analysis.

*More details to come*
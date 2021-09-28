# Announcements MicroService
[![Code quality checks](https://github.com/anastasiia-a/announcement-ms/actions/workflows/checks.yml/badge.svg)](https://github.com/anastasiia-a/announcement-ms/actions/workflows/checks.yml)

## Overview
A small serverless application (MicroService) which exposes JSON formatted REST APIs which allow for storing and retrieving announcements.


### Solutions and standards

* OpenAPI 3.0
* Formation Scripts
* AWS Serverless services
* Postman

### The application consists of
* AWS REST API Gateway
* 2 Lambdas
* DynamoDB Table

## How to deploy
1. [Install aws cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

2. Clone the repository
```
git clone https://github.com/anastasiia-a/announcement-ms
```
3. Export the needed enviroment variables

|№|command|description|
|-|-|-|
|1|`export AWS_ACCESS_KEY_ID=`|access for AWS |
|2|`export AWS_SECRET_ACCESS_KEY=`|access for AWS|
|3|`export AWS_DEFAULT_REGION=`|access for AWS|
|4|`export S3_BUCKET=`|for 'deploy.sh'|
|5|`export STACK_NAME=`|for 'deploy.sh'|

4. Run the following command
```
./deploy.sh
```

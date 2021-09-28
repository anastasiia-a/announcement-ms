# Announcements MicroService
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-39/)
[![Code quality checks](https://github.com/anastasiia-a/announcement-ms/actions/workflows/checks.yml/badge.svg)](https://github.com/anastasiia-a/announcement-ms/actions/workflows/checks.yml)

## Overview
A small serverless application (MicroService) which exposes JSON formatted REST APIs which allow for storing and retrieving announcements. The application consists of `DynamoDB Table`, `Lambda` to read data from the DB, `Lambda` to write data to the DB, `API Gateway`.


### Solutions and standards

* OpenAPI 3.0
* Formation Scripts
* AWS Serverless services
* Postman Collections


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

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
3. Export needed environment variables
```
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_DEFAULT_REGION=
export S3_BUCKET=
export STACK_NAME=
```

4. Run the following command for deploying in AWS
```
./deploy.sh
```
5. Command to deleting a stack
```
aws cloudformation delete-stack --stack-name ${STACK_NAME}

```
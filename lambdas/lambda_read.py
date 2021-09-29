import json
import logging
import os

import boto3

TABLE_NAME = os.environ["TABLE"]

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


def lambda_handler(event, context):
    """Read all items from the dynamodb table."""

    try:
        client = boto3.resource("dynamodb")
        table = client.Table(TABLE_NAME)
        scan = table.scan()
        announcements = scan["Items"]
        logging.info(f">[INFO]- Successfully scan items from the table '{TABLE_NAME}'")

        while "LastEvaluatedKey" in scan:
            scan = table.scan(ExclusiveStartKey=scan.get("LastEvaluatedKey"))
            announcements.extend(scan["Items"])

        logging.info(">[INFO]- Successfully read all announcements")

        return {
            "statusCode": 200,
            "body": json.dumps(announcements, ensure_ascii=False, default=str),
        }

    except Exception as exception:
        logging.error(f">[ERROR]- Exception {exception}")
        return {"statusCode": 500, "body": json.dumps("Internal server error")}

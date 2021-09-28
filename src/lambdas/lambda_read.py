import json
import logging
import os

import boto3

TABLE_NAME = os.environ["TABLE"]

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def lambda_handler(event, context):
    """Read all items from the dynamodb table."""

    try:
        client = boto3.resource("dynamodb")
        table = client.Table(TABLE_NAME)
        logging.info(f">[INFO]- Successfully connected to the table '{TABLE_NAME}'")
        table_scan = table.scan()
        announcements = table_scan["Items"]

        while "LastEvaluatedKey" in table_scan:
            table_scan = table.scan(
                ExclusiveStartKey=table_scan.get("LastEvaluatedKey")
            )
            announcements.extend(table_scan["Items"])

        logging.info(">[INFO]- Successfully read all announcements")
        return {
            "statusCode": 200,
            "body": json.dumps(announcements, ensure_ascii=False, default=str),
        }

    except Exception as exception:
        logging.error(f">[ERROR]- Exception {exception}")
        return {"statusCode": 500, "body": json.dumps("Internal server error")}

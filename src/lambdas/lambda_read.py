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
        announcements = table.scan()["Items"]

        all_announcements = []
        for announcement in announcements:
            all_announcements.append(
                {
                    "title": announcement.get("title"),
                    "description": announcement.get("description"),
                    "date": announcement.get("date"),
                }
            )
        logging.info(">[INFO]- Successfully read all announcements")
        return {"statusCode": 200, "body": json.dumps(all_announcements)}

    except Exception as exception:
        logging.error(f">[ERROR]- Exception {exception}")
        return {"statusCode": 500, "body": json.dumps("Internal server error")}

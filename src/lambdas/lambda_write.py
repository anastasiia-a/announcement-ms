import json
import logging
import os
import uuid

import boto3

TABLE_NAME = os.environ["TABLE"]

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def lambda_handler(event, context) -> json:
    """Create a new item in the dynamodb table."""

    try:
        body = event.get("body", {})
        body = json.loads(body, strict=False)
        logging.info(f">[INFO]'- Call with body: {body}")

        title = body.get("title")
        date = body.get("date")
        description = body.get("description", "")

        if not all([title, date]):
            logging.error(
                ">[ERROR]'- Some mandatory parameters are missing (title, date)!"
            )
            return {
                "statusCode": 400,
                "body": json.dumps(
                    "Some mandatory parameters are missing (title, date)!"
                ),
            }

        client = boto3.resource("dynamodb")
        table = client.Table(TABLE_NAME)
        new_item = {
            "uuid": f"{uuid.uuid4()}",
            "title": title,
            "description": description,
            "date": date,
        }
        table.put_item(Item=new_item)
        item_without_uuid = {
            "title": new_item["title"],
            "description": new_item["description"],
            "date": new_item["date"],
        }
        logging.info(
            f">[INFO] - New item with uuid={new_item['uuid']} "
            f"in table '{TABLE_NAME}' created successful."
        )
        return {
            "statusCode": 201,
            "body": json.dumps(f"New item created successfully\n{item_without_uuid}"),
        }

    except Exception as exception:
        logging.error(f">[ERROR] - Exception {exception}")
        return {"statusCode": 500, "body": json.dumps("Internal server error")}

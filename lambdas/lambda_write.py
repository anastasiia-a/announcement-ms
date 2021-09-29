import json
import logging
import os
import uuid

import boto3

TABLE_NAME = os.environ["TABLE"]
MISSING_PARAMETERS_MESSAGE = "Some mandatory parameters are missing (title, date)!"

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def lambda_handler(event, context) -> json:
    """
    Create a new item in the dynamodb table.
    Allow creating duplicates.
    """

    try:
        body = event.get("body", "{}")
        body = json.loads(body, strict=False)
        logging.info(f">[INFO]'- Call with body: {body}")

        title = body.get("title")
        date = body.get("date")
        description = body.get("description", "")

        if not all([title, date]):
            logging.error(f">[ERROR]'- {MISSING_PARAMETERS_MESSAGE}")
            return {"statusCode": 400, "body": json.dumps(MISSING_PARAMETERS_MESSAGE)}

        client = boto3.resource("dynamodb")
        table = client.Table(TABLE_NAME)
        new_item = {
            "uuid": f"{uuid.uuid4()}",
            "title": title,
            "description": description,
            "date": date,
        }
        table.put_item(Item=new_item)
        logging.info(
            f">[INFO] - New item with uuid={new_item['uuid']} "
            f"in table '{TABLE_NAME}' created successful."
        )

        return {"statusCode": 201, "body": json.dumps(f"{new_item}")}

    except Exception as exception:
        logging.error(f">[ERROR] - Exception {exception}")
        return {"statusCode": 500, "body": json.dumps("Internal server error")}

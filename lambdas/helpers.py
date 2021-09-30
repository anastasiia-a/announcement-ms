import json
import logging
import os
import uuid
from typing import Optional

import boto3
from aws_lambda_powertools.utilities.parser import BaseModel, parse
from exceptions import BlankRequestBody

TABLE_NAME = os.environ["TABLE"]
MISSING_PARAMETERS_MESSAGE = "Some mandatory body parameters are missing (title, date)!"
INCORRECT_PARAMETERS_MESSAGE = "Body parameters are incorrect"
BLANK_REQUEST_BODY_MESSAGE = "Blank Request Body"

logging.getLogger()
logging.basicConfig(
    format="%(asctime)s >[%(levelname)s] %(message)s", level=logging.INFO
)


class Announcement(BaseModel):
    """Model for creating announcements
    and parsing the body of the request."""

    title: str
    date: str
    description: Optional[str]


def get_dynamodb_table(table_name):
    """Return AWS DynamoDB Table"""
    client = boto3.resource("dynamodb")
    table = client.Table(table_name)
    return table


def create_new_table_item(event):
    """
    Create a new item in the dynamodb table.
    Allow creating duplicates.
    :param event: lambda event
    :return: new created item in json format
    """
    body = event.get("body")

    if not body:
        logging.error(f"{BLANK_REQUEST_BODY_MESSAGE}")
        raise BlankRequestBody

    body = json.loads(body)
    logging.info(f"Call with body: {body}")

    payload = {
        "title": body.get("title"),
        "date": body.get("date"),
        "description": body.get("description"),
    }

    parsed_payload: Announcement = parse(event=payload, model=Announcement)
    table = get_dynamodb_table(TABLE_NAME)
    new_item = {
        "uuid": f"{uuid.uuid4()}",
        "title": parsed_payload.title,
        "description": parsed_payload.description,
        "date": parsed_payload.date,
    }

    table.put_item(Item=new_item)
    logging.info(
        f"New item uuid={new_item['uuid']} in table {TABLE_NAME} created successful"
    )

    return new_item


def read_table_items():
    """
    Read all items from the dynamodb table.
    """

    table = get_dynamodb_table(TABLE_NAME)
    scan = table.scan()
    announcements = scan["Items"]
    logging.info(f"Successfully scan items from the table '{TABLE_NAME}'")

    while "LastEvaluatedKey" in scan:
        scan = table.scan(ExclusiveStartKey=scan.get("LastEvaluatedKey"))
        announcements.extend(scan["Items"])

    logging.info("Successfully read all items")
    return announcements

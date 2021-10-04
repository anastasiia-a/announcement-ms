import logging
import os
from typing import Optional
from uuid import uuid4

import boto3
from aws_lambda_powertools.utilities.parser import BaseModel, Field, parse
from exceptions import BlankRequestBody

TABLE_NAME = os.environ["TABLE"]
MISSING_PARAMETERS_MESSAGE = "Some mandatory body parameters are missing (title, date)!"
INCORRECT_PARAMETERS_MESSAGE = "Body parameters are incorrect"
BLANK_REQUEST_BODY_MESSAGE = "Blank Request Body"

logging.getLogger()
logging.basicConfig(
    format="%(asctime)s >[%(levelname)s] %(message)s", level=logging.INFO
)


def get_new_str_uuid4():
    """Generate a new uuid in string format."""
    return str(uuid4())


class Announcement(BaseModel):
    """Model for creating announcements
    and parsing the body of the request."""

    uuid: str = Field(default_factory=get_new_str_uuid4)
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

    logging.info(f"Call with body: {body}")

    announcement: Announcement = parse(event=body, model=Announcement)
    new_announcement = announcement.dict()
    table = get_dynamodb_table(TABLE_NAME)

    table.put_item(Item=new_announcement)
    logging.info(
        f"New item uuid={new_announcement['uuid']} "
        f"in table {TABLE_NAME} created successful"
    )

    return new_announcement


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

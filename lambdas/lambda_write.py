import json
import logging

from aws_lambda_powertools.utilities.parser import ValidationError
from exceptions import BlankRequestBody
from helpers import (
    INCORRECT_PARAMETERS_MESSAGE,
    MISSING_PARAMETERS_MESSAGE,
    create_new_table_item,
)

logging.getLogger()
logging.basicConfig(
    format="%(asctime)s >[%(levelname)s] %(message)s", level=logging.INFO
)


def lambda_handler(event, context):
    """
    Create a new item in the dynamodb table.
    Allow creating duplicates.
    """

    try:
        created_item = create_new_table_item(event)
        return {"statusCode": 201, "body": json.dumps(f"{created_item}")}

    except BlankRequestBody as exception:
        logging.error(f"{exception}")
        return {"statusCode": 400, "body": json.dumps(MISSING_PARAMETERS_MESSAGE)}

    except ValidationError as exception:
        logging.error(f"{exception}")
        return {"statusCode": 400, "body": json.dumps(INCORRECT_PARAMETERS_MESSAGE)}

    except Exception as exception:
        logging.error(f"{exception}")
        return {"statusCode": 500, "body": json.dumps("Internal server error")}

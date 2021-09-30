import json
import logging

from helpers import read_table_items

logging.getLogger()
logging.basicConfig(
    format="%(asctime)s >[%(levelname)s] %(message)s", level=logging.INFO
)


def lambda_handler(event, context):
    """Read all items from the dynamodb table."""

    try:
        announcements = read_table_items()
        return {
            "statusCode": 200,
            "body": json.dumps(announcements, ensure_ascii=False, default=str),
        }

    except Exception as exception:
        logging.error(f"Exception {exception}")
        return {"statusCode": 500, "body": json.dumps("Internal server error")}

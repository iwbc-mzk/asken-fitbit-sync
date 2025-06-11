from typing import Optional
import json
from datetime import datetime
import copy
import os

import requests
import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

from .asken import Asken
from .fitbit import Fitbit
from .asken_fitbit_sync import AskenFitbitSync
from .const import DAILY_MEAL_TYPE_ID_LIST
from .utils import get_logger
from .mock import FitbitMock


logger = get_logger(__name__)


def get_secret_manager_client():
    session = boto3.session.Session()
    return session.client(service_name="secretsmanager", region_name="ap-northeast-1")


def get_secret():
    """
    Get credentials from AWS Secrets Manager or local file based on the environment.
    Returns:
        dict: Credentials containing mail, password, client_id, access_token, and refresh_token.
    """
    # ローカル開発用
    if os.environ["ENV"] == "local":
        with open("src/.credentials.json", "r") as f:
            return json.load(f)

    client = get_secret_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId="askenFitbitSync")
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return json.loads(get_secret_value_response["SecretString"])


def refresh_token_callback(access_token: str, refresh_token: str):
    logger.debug("Refreshing token callback start.")
    client = get_secret_manager_client()
    credencials = get_secret()
    credencials["access_token"] = access_token
    credencials["refresh_token"] = refresh_token
    client.update_secret(
        SecretId="askenFitbitSync", SecretString=json.dumps(credencials)
    )
    logger.debug("Refreshing token callback end.")


def main(
    date: str,
    mail: str,
    password: str,
    client_id: str,
    access_token: str,
    refresh_token: str,
    meal_type_id_list: list[int] = DAILY_MEAL_TYPE_ID_LIST,
):
    logger.info(f"Syncing food logs for date: {date}")

    asken = Asken(mail, password)
    if os.environ["ENV"] == "local":
        fitbit: Fitbit = FitbitMock()
    else:
        fitbit = Fitbit(
            client_id,
            access_token,
            refresh_token,
            callback_on_token_refreshed=refresh_token_callback,
        )
    syncer = AskenFitbitSync(asken, fitbit)
    syncer.sync_food_logs(date, meal_type_id_list)

    logger.info(f"Food logs synced successfully for date: {date}")


def lambda_handler(event, context):
    logger.info("Starting Asken-Fitbit sync...")

    date = event.get("date", datetime.now().strftime("%Y-%m-%d"))
    credencials = get_secret()
    try:
        main(
            date=date,
            mail=credencials["mail"],
            password=credencials["password"],
            client_id=credencials["client_id"],
            access_token=credencials["access_token"],
            refresh_token=credencials["refresh_token"],
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    else:
        logger.info("Asken-Fitbit sync completed.")

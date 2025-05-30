from typing import Optional
import json

import requests

from asken import Asken
from fitbit import Fitbit
from asken_fitbit_sync import AskenFitbitSync
from const import DAILY_MEAL_TYPE_ID_LIST
from utils import get_logger

CREDENCIALS_PATH = ".env"

logger = get_logger(__name__)


def retry_after_refresh_token(func):
    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            if e.response.status_code == 401:
                logger.warning("Access token expired, refreshing...")

                fitbit = Fitbit(
                    kwargs["client_id"], kwargs["access_token"], kwargs["refresh_token"]
                )
                response = fitbit.refresh_access_token()
                kwargs["access_token"] = response["access_token"]
                kwargs["refresh_token"] = response["refresh_token"]
                json.dump(
                    kwargs, open(CREDENCIALS_PATH, "w"), indent=4, ensure_ascii=False
                )

                logger.info("Access token refreshed successfully.")

                func(*args, **kwargs)
            else:
                raise e

    return wrapped


@retry_after_refresh_token
def main(
    date: str,
    mail: str,
    password: str,
    client_id: str,
    access_token: str,
    refresh_token: str,
    meal_type_id_list: Optional[list[int]] = DAILY_MEAL_TYPE_ID_LIST,
):
    logger.info(f"Syncing food logs for date: {date}")

    asken = Asken(mail, password)
    fitbit = Fitbit(client_id, access_token, refresh_token)
    syncer = AskenFitbitSync(asken, fitbit)
    syncer.sync_food_logs(date, meal_type_id_list)

    logger.info(f"Food logs synced successfully for date: {date}")


if __name__ == "__main__":
    logger.info("Starting Asken-Fitbit sync...")

    credencials = json.load(open(CREDENCIALS_PATH, "r"))
    date = "2025-05-30"
    try:
        main(
            date=date,
            mail=credencials["asken_mail"],
            password=credencials["asken_password"],
            client_id=credencials["fitbit_client_id"],
            access_token=credencials["fitbit_access_token"],
            refresh_token=credencials["fitbit_refresh_token"],
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    logger.info("Asken-Fitbit sync completed.")

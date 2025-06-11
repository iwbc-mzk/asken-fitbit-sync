from typing import Optional, Protocol, Any
from collections.abc import Callable

import requests

from .models.fitbit import (
    GetFoodLogResponse,
    UpdateFoodLogParams,
    CreateFoodLogParams,
)
from src.utils import get_logger


logger = get_logger(__name__)


type access_token = str
type refresh_token = str


class Fitbit:
    def __init__(
        self,
        client_id: str,
        access_token: str,
        refresh_token: str,
        auto_token_refresh: bool = True,
        callback_on_token_refreshed: Optional[
            Callable[[access_token, refresh_token], Any]
        ] = None,
    ):
        self._client_id = client_id
        self._access_token: str = access_token
        self._refresh_token: str = refresh_token
        self._auto_token_refresh = auto_token_refresh
        self._callback_on_token_refreshed = callback_on_token_refreshed
        self._host = "https://api.fitbit.com"

    @staticmethod
    def _auto_token_refresh_decorator(func):
        def wrapper(self: "Fitbit", *args, **kwargs):
            try:
                try:
                    return func(self, *args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if (
                        # requests.Responseのbool変換値はステータスコードが400未満の時にTrueになるため以下のように存在チェックする必要あり
                        e.response is not None
                        and e.response.status_code == 401
                        and self._auto_token_refresh
                    ):
                        logger.warning("Access token expired, refreshing...")

                        self.refresh_access_token()

                        logger.info("Access token refreshed successfully.")

                        return func(self, *args, **kwargs)
                    else:
                        raise
            except Exception as e:
                logger.error(
                    f"Unexpected error: {e} (func={func.__name__}, args={args}, kwargs={kwargs})",
                    exc_info=True,
                )
                raise

        return wrapper

    @_auto_token_refresh_decorator
    def fetch_food_log(self, date: str) -> GetFoodLogResponse:
        url = f"{self._host}/1/user/-/foods/log/date/{date}.json"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "accept-language": "ja_JP",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        return GetFoodLogResponse(**response.json())

    @_auto_token_refresh_decorator
    def create_food_log(self, params: CreateFoodLogParams) -> dict:
        url = f"{self._host}/1/user/-/foods/log.json"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "accept-language": "ja_JP",
        }

        response = requests.post(url, headers=headers, params=params.model_dump())
        response.raise_for_status()  # Raise an error for bad responses

        return response.json()

    @_auto_token_refresh_decorator
    def update_food_log(self, food_log_id: int, params: UpdateFoodLogParams) -> dict:
        url = f"{self._host}/1/user/-/foods/log/{food_log_id}.json"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "accept-language": "ja_JP",
        }
        response = requests.post(url, headers=headers, params=params.model_dump())
        response.raise_for_status()

        return response.json()

    @_auto_token_refresh_decorator
    def delete_food_log(self, food_log_id: int) -> requests.Response:
        url = f"{self._host}/1/user/-/foods/log/{food_log_id}.json"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

        return response

    def refresh_access_token(self) -> dict:
        url = f"{self._host}/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        body = {
            "client_id": self._client_id,
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }

        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()  # Raise an error for bad responses

        tokens = response.json()
        self._access_token = tokens["access_token"]
        self._refresh_token = tokens["refresh_token"]

        if self._callback_on_token_refreshed:
            self._callback_on_token_refreshed(self._access_token, self._refresh_token)

        return tokens

import requests

from src.models.fitbit import (
    GetFoodLogResponse,
    UpdateFoodLogParams,
    CreateFoodLogParams,
)
from const import FITBIT_API_URL


class Fitbit:
    def __init__(self, client_id: str, access_token: str, refresh_token: str):
        self._client_id = client_id
        self._access_token = access_token
        self._refresh_token = refresh_token

    def fetch_food_log(self, date: str) -> GetFoodLogResponse:
        url = f"{FITBIT_API_URL}/1/user/-/foods/log/date/{date}.json"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "accept-language": "ja_JP",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        return GetFoodLogResponse(**response.json())

    def create_food_log(self, params: CreateFoodLogParams) -> dict:
        url = f"{FITBIT_API_URL}/1/user/-/foods/log.json"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "accept-language": "ja_JP",
        }

        response = requests.post(url, headers=headers, params=params.model_dump())
        response.raise_for_status()  # Raise an error for bad responses

        return response.json()

    def update_food_log(self, food_log_id: int, params: UpdateFoodLogParams) -> dict:
        url = f"{FITBIT_API_URL}/1/user/-/foods/log/{food_log_id}.json"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "accept-language": "ja_JP",
        }
        response = requests.post(url, headers=headers, params=params.model_dump())
        response.raise_for_status()

        return response.json()

    def delete_food_log(self, food_log_id: int) -> requests.Response:
        url = f"{FITBIT_API_URL}/1/user/-/foods/log/{food_log_id}.json"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

        return response

    def refresh_access_token(self) -> dict:
        url = f"{FITBIT_API_URL}/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        body = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }

        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()  # Raise an error for bad responses

        return response.json()

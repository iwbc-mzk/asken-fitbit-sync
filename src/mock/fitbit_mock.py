import requests
from unittest.mock import patch, MagicMock

from ..models.fitbit import (
    GetFoodLogResponse,
    UpdateFoodLogParams,
    CreateFoodLogParams,
)
from ..fitbit import Fitbit
from ..utils import get_logger


logger = get_logger(__name__)


class FitbitMock(Fitbit):
    """
    Mock class for Fitbit API to simulate responses for testing purposes.
    This class overrides methods to return predefined responses instead of making actual API calls.
    It is useful for unit tests where you want to avoid network calls and control the responses.
    """

    def __init__(self):
        super().__init__("test_client_id", "test_access_token", "test_refresh_token")

    @patch("requests.get")
    def fetch_food_log(self, date: str, mock: MagicMock) -> GetFoodLogResponse:
        res = requests.Response()
        res.status_code = 200
        res._content = b"""{
            "foods": [
                {
                    "isFavorite": true,
                    "logDate": "2019-03-21",
                    "logId": 17406206369,
                    "loggedFood": {
                        "accessLevel": "PUBLIC",
                        "amount": 1,
                        "brand": "Subway",
                        "calories": 280,
                        "foodId": 14022778,
                        "locale": "en_US",
                        "mealTypeId": 3,
                        "name": "6 inch Turkey Breast",
                        "unit": {"id": 296, "name": "sandwich", "plural": "sandwiches"},
                        "units": [296, 226, 180, 147, 389]
                    },
                    "nutritionalValues": {
                        "calories": 280,
                        "carbs": 46,
                        "fat": 3.5,
                        "fiber": 5,
                        "protein": 18,
                        "sodium": 760
                    }
                }
            ],
            "goals": {"calories": 2910},
            "summary": {
                "calories": 280,
                "carbs": 46,
                "fat": 3.5,
                "fiber": 5,
                "protein": 18,
                "sodium": 760,
                "water": 0
            }
        }"""
        mock.return_value = res

        return super().fetch_food_log(date)

    @patch("requests.post")
    def create_food_log(self, params: CreateFoodLogParams, mock: MagicMock) -> dict:
        res = requests.Response()
        res.status_code = 201
        res._content = b"""{
            "foodDay": {
                "date": "2019-03-21",
                "summary": {
                    "calories": 1224,
                    "carbs": 165.85,
                    "fat": 48.13,
                    "fiber": 17.75,
                    "protein": 30.75,
                    "sodium": 1588.75,
                    "water": 1892.7099609375
                }
            },
            "foodLog": {
                "isFavorite": true,
                "logDate": "2019-03-21",
                "logId": 17406014466,
                "loggedFood": {
                    "accessLevel": "PUBLIC",
                    "amount": 2.55,
                    "brand": "",
                    "calories": 944,
                    "foodId": 82294,
                    "locale": "en_US",
                    "mealTypeId": 3,
                    "name": "Chips",
                    "unit": {
                        "id": 304,
                        "name": "serving",
                        "plural": "servings"
                    },
                    "units": [
                        304,
                        226,
                        180,
                        147,
                        389
                    ]
                },
                "nutritionalValues": {
                    "calories": 944,
                    "carbs": 119.85,
                    "fat": 44.63,
                    "fiber": 12.75,
                    "protein": 12.75,
                    "sodium": 828.75
                }
            }
        }"""
        mock.return_value = res

        return super().create_food_log(params)

    @patch("requests.post")
    def update_food_log(
        self, food_log_id: int, params: UpdateFoodLogParams, mock: MagicMock
    ) -> dict:
        res = requests.Response()
        res.status_code = 201
        res._content = b"""{
            "foodLog": {
                "isFavorite": false,
                "logDate": "2020-06-10",
                "logId": 22100146659,
                "loggedFood": {
                    "accessLevel": "PUBLIC",
                    "amount": 1,
                    "brand": "",
                    "calories": 130,
                    "foodId": 81409,
                    "locale": "en_US",
                    "mealTypeId": 1,
                    "name": "Apple",
                    "unit": {
                        "id": 179,
                        "name": "large",
                        "plural": "larges"
                    },
                    "units": [
                        204,
                        179,
                        226,
                        180,
                        147,
                        389
                    ]
                },
                "nutritionalValues": {
                    "calories": 130,
                    "carbs": 35.75,
                    "fat": 0,
                    "fiber": 8.13,
                    "protein": 0,
                    "sodium": 0
                }
            }
        }"""
        mock.return_value = res

        return super().update_food_log(food_log_id, params)

    @patch("requests.delete")
    def delete_food_log(self, food_log_id: int, mock: MagicMock) -> requests.Response:
        res = requests.Response()
        res.status_code = 204
        mock.return_value = res

        return super().delete_food_log(food_log_id)

    @patch("requests.post")
    def refresh_access_token(self, mock: MagicMock) -> dict:
        res = requests.Response()
        res.status_code = 200
        res._content = b"""{
            "access_token": "eyJhbGciOiJIUzI1...",
            "expires_in": 28800,
            "refresh_token": "c643a63c072f0f05478e9d18b991db80ef6061e...",
            "token_type": "Bearer",
            "user_id": "GGNJL9"
        }"""
        mock.return_value = res

        return super().refresh_access_token()

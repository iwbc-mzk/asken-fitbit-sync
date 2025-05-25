import base64
from typing import Optional

import requests
from pydantic import BaseModel

from models.food_log import FoodLogResponse


FITBIT_API_URL = "https://api.fitbit.com"
def refresh_access_token(
    client_id: str, client_secret: str, refresh_token: str
) -> dict:
    url = f"{FITBIT_API_URL}/oauth2/token"
    authorization = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {authorization}",
        "Accept": "application/json",
    }
    body = {
        "client_id": client_id,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

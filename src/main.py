import base64
from typing import Optional

import requests
from pydantic import BaseModel

from models.food_log import FoodLogResponse
from utils import micrograms_to_iu, salt_g_to_sodium_mg


FITBIT_API_URL = "https://api.fitbit.com"
class FoodLogParams(BaseModel):
    foodId: Optional[int] = None
    foodName: Optional[str] = None
    mealTypeId: int
    unitId: int
    amount: int
    date: str
    favorite: Optional[bool] = None
    brandName: Optional[str] = None
    calories: Optional[int] = None
    caloriesFromFat: Optional[int] = None
    totalFat: Optional[float] = None  # 脂質(g)
    transFat: Optional[float] = None  # トランス脂肪酸(g)
    saturatedFat: Optional[float] = None  # 飽和脂肪酸(g)
    cholesterol: Optional[float] = None  # コレステロール(mg)
    sodium: Optional[float] = None  # ナトリウム(mg)
    potassium: Optional[float] = None  # カリウム(mg)
    totalCarbohydrate: Optional[float] = None  # 炭水化物(g)
    dietaryFiber: Optional[float] = None  # 食物繊維(g)
    sugars: Optional[float] = None  # 糖質(g)
    protein: Optional[float] = None  # タンパク質(g)
    vitaminA: Optional[float] = None  # ビタミンA(IU)
    vitaminB6: Optional[float] = None  # ビタミンB6
    vitaminB12: Optional[float] = None  # ビタミンB12
    vitaminC: Optional[float] = None  # ビタミンC(mg)
    vitaminD: Optional[float] = None  # ビタミンD(IU)
    vitaminE: Optional[float] = None  # ビタミンE(IU)
    biotin: Optional[float] = None  # ビオチン(mg)
    folicAcid: Optional[float] = None  # 葉酸(mg)
    niacin: Optional[float] = None  # ナイアシン(mg)
    pantothenicAcid: Optional[float] = None  # パントテン酸(mg)
    riboflavin: Optional[float] = None  # リボフラビン(mg)
    thiamin: Optional[float] = None  # チアミン(mg)
    calcium: Optional[float] = None  # カルシウム(g)
    copper: Optional[float] = None  # 銅(g)
    iron: Optional[float] = None  # 鉄分(mg)
    magnesium: Optional[float] = None  # マグネシウム(mg)
    phosphorus: Optional[float] = None  # リン(mg)
    iodine: Optional[float] = None  # ヨウ素(mcg)
    zinc: Optional[float] = None  # 亜鉛(mg)


def get_food_log(access_token: str, date: str) -> FoodLogResponse:
    url = f"{FITBIT_API_URL}/1/user/-/foods/log/date/{date}.json"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "accept-language": "ja_JP",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return FoodLogResponse(**response.json())


def create_food_log(access_token: str, params: FoodLogParams) -> dict:
    url = f"{FITBIT_API_URL}/1/user/-/foods/log.json"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "accept-language": "ja_JP",
    }

    response = requests.post(url, headers=headers, params=params.model_dump())
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


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

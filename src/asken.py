from bs4 import BeautifulSoup
from pydantic import BaseModel
import requests

from utils import remove_unit


ASKEN_URL = "https://www.asken.jp"


class FoodLog(BaseModel):
    date: str
    meal_type_id: int
    calories: float  # カロリー(kcal)
    protein: float  # タンパク質(g)
    fat: float  # 脂質(g)
    carbs: float  # 炭水化物(g)
    calcium: float  # カルシウム(mg)
    magnesium: float  # マグネシウム(mg)
    iron: float  # 鉄分(mg)
    zinc: float  # 亜鉛(mg)
    vitamin_a: float  # ビタミンA(μg)
    vitamin_d: float  # ビタミンD(μg)
    vitamin_b1: float  # ビタミンB1(mg)
    vitamin_b2: float  # ビタミンB2(mg)
    vitamin_b6: float  # ビタミンB6(mg)
    vitamin_c: float  # ビタミンC(mg)
    fiber: float  # 食物繊維(g)
    saturatedFat: float  # 飽和脂肪酸(g)
    solt: float  # 食塩相当量(g)


NUTRITIONS = {
    "エネルギー": "calories",
    "タンパク質": "protein",
    "脂質": "fat",
    "炭水化物": "carbs",
    "カルシウム": "calcium",
    "マグネシウム": "magnesium",
    "鉄": "iron",
    "亜鉛": "zinc",
    "ビタミンA": "vitamin_a",
    "ビタミンD": "vitamin_d",
    "ビタミンB1": "vitamin_b1",
    "ビタミンB2": "vitamin_b2",
    "ビタミンB6": "vitamin_b6",
    "ビタミンC": "vitamin_c",
    "食物繊維": "fiber",
    "飽和脂肪酸": "saturatedFat",
    "塩分": "solt",
}


class Asken:
    def __init__(self, email: str, password: str):
        self.session = self.login(email, password)

    def login(self, email: str, password: str) -> requests.Session:
        """Login to Asken and return a session."""

        login_url = f"{ASKEN_URL}/login/"
        session = requests.Session()

        payload = {
            "_method": "POST",
            "data[_Token][key]": "b5e46df4f20835456a0e20c07bc0d05fab17bceae4869081bddb3e419d8a476b5d465721a6fdb998e379eedb1f813d4f4accc4b4ccce5c9ce7e07746c2a02846",
            "data[CustomerMember][email]": email,
            "data[CustomerMember][passwd_plain]": password,
            "data[CustomerMember][autologin]": 1,
            "data[Submit][submit][x]": 102,
            "data[Submit][submit][x]": 19,
        }

        headers = {
            # User-Agentでアクセス制限をしているようで指定しないと403エラーが返ってくる
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        }

        response = session.post(login_url, headers=headers, data=payload)
        response.raise_for_status()  # Check if the request was successful

        return session

    def fetch_food_log(self, date: str, meal_type_id: int) -> FoodLog:
        """
        Fetch food log for a specific date and meal type.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
            meal_type_id (int): Meal type ID (1: 朝食, 2: 昼食, 3: 夕食).
        Returns:
            FoodLog: Parsed food log data.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        }
        advice_url = f"{ASKEN_URL}/wsp/advice/{date}/{meal_type_id + 2}"
        response = self.session.get(url=advice_url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, "html.parser")

            nutrition_name = nutrition_ele.find("li", class_="title").text.strip()
            nutrition_value = nutrition_ele.find("li", class_="val").text.strip()

            if nutrition_name in NUTRITIONS:
                nutritions[NUTRITIONS[nutrition_name]] = remove_unit(nutrition_value)

        food_log = FoodLog(**nutritions)

        return food_log

from typing import Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel
import requests

from utils import remove_unit
from const import MEAL_TYPES


ASKEN_URL = "https://www.asken.jp"


class FoodLog(BaseModel):
    date: str
    meal_type_id: int
    calories: float = 0.0  # カロリー(kcal)
    protein: float = 0.0  # タンパク質(g)
    fat: float = 0.0  # 脂質(g)
    carbs: float = 0.0  # 炭水化物(g)
    calcium: float = 0.0  # カルシウム(mg)
    magnesium: float = 0.0  # マグネシウム(mg)
    iron: float = 0.0  # 鉄分(mg)
    zinc: float = 0.0  # 亜鉛(mg)
    vitamin_a: float = 0.0  # ビタミンA(μg)
    vitamin_d: float = 0.0  # ビタミンD(μg)
    vitamin_b1: float = 0.0  # ビタミンB1(mg)
    vitamin_b2: float = 0.0  # ビタミンB2(mg)
    vitamin_b6: float = 0.0  # ビタミンB6(mg)
    vitamin_c: float = 0.0  # ビタミンC(mg)
    fiber: float = 0.0  # 食物繊維(g)
    saturatedFat: float = 0.0  # 飽和脂肪酸(g)
    solt: float = 0.0  # 食塩相当量(g)
    logged: bool = False  # 食事記録が登録済かどうか


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

    @staticmethod
    def _headers() -> dict:
        """Return headers for requests."""
        return {
            # User-Agentでアクセス制限をしているようで指定しないと403エラーが返ってくる
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        }

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

        response = session.post(login_url, headers=self._headers(), data=payload)
        response.raise_for_status()  # Check if the request was successful

        return session

    def fetch_food_log(self, date: str, meal_type_id: Optional[int] = None) -> FoodLog:
        """
        Fetch food log for a specific date.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
            meal_type_id (Optional[int]): Meal type ID (1: 朝食, 2: 昼食, 3: 夕食, 4: 間食, 5: 1日分). If None, fetches all total food log.
        Returns:
            FoodLog: Parsed food log data.
        """
        if meal_type_id in [1, 2, 3]:
            return self.fetch_one_meal_log(date, meal_type_id)
        elif meal_type_id == 4:
            return self.fetch_snack_log(date)
        elif meal_type_id == 5:
            return self.fetch_daily_food_log(date)

    def fetch_one_meal_log(self, date: str, meal_type_id: int) -> FoodLog:
        """
        Fetch one meal log for a specific date and meal type.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
            meal_type_id (int): Meal type ID (1: 朝食, 2: 昼食, 3: 夕食).
        Returns:
            FoodLog: Parsed food log data.
        """
        advice_url = (
            f"{ASKEN_URL}/wsp/advice/{date}/{MEAL_TYPES[meal_type_id]['asken_id']}"
        )
        response = self.session.get(url=advice_url, headers=self._headers())
        response.raise_for_status()

        html = response.text
        if "食事記録が無いためアドバイスが計算できません" in html:
            return FoodLog(**{"date": date, "meal_type_id": meal_type_id})

        nutritions = self._scrape_food_log(html)
        nutritions["meal_type_id"] = meal_type_id
        nutritions["date"] = date

        food_log = FoodLog(**nutritions)
        food_log.logged = True

        return food_log

    def fetch_daily_food_log(self, date: str) -> FoodLog:
        """
        Fetch daily food log for a specific date.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
        Returns:
            FoodLog: Parsed food log data.
        """
        advice_url = f"{ASKEN_URL}/wsp/advice/{date}"
        response = self.session.get(url=advice_url, headers=self._headers())
        response.raise_for_status()

        html = response.text
        if "食事記録が無いためアドバイスが計算できません" in html:
            return FoodLog()

        nutritions = self._scrape_food_log(html)
        nutritions["meal_type_id"] = 5  # Set meal type ID for daily log
        nutritions["date"] = date

        food_log = FoodLog(**nutritions)
        food_log.logged = True

        return food_log

    def fetch_snack_log(self, date: str) -> FoodLog:
        """
        Fetch snack log for a specific date.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
        Returns:
            FoodLog: Parsed snack log data.
        """
        nutritions = self.fetch_daily_food_log(date).model_dump()
        nutritions["meal_type_id"] = 4  # Set meal type ID for snack log
        for meal_type_id in [1, 2, 3]:
            one_meal_log = self.fetch_one_meal_log(date, meal_type_id).model_dump()
            nutritions["calories"] -= one_meal_log["calories"]
            nutritions["protein"] -= one_meal_log["protein"]
            nutritions["fat"] -= one_meal_log["fat"]
            nutritions["carbs"] -= one_meal_log["carbs"]
            nutritions["calcium"] -= one_meal_log["calcium"]
            nutritions["magnesium"] -= one_meal_log["magnesium"]
            nutritions["iron"] -= one_meal_log["iron"]
            nutritions["zinc"] -= one_meal_log["zinc"]
            nutritions["vitamin_a"] -= one_meal_log["vitamin_a"]
            nutritions["vitamin_d"] -= one_meal_log["vitamin_d"]
            nutritions["vitamin_b1"] -= one_meal_log["vitamin_b1"]
            nutritions["vitamin_b2"] -= one_meal_log["vitamin_b2"]
            nutritions["vitamin_b6"] -= one_meal_log["vitamin_b6"]
            nutritions["vitamin_c"] -= one_meal_log["vitamin_c"]
            nutritions["fiber"] -= one_meal_log["fiber"]
            nutritions["saturatedFat"] -= one_meal_log["saturatedFat"]
            nutritions["solt"] -= one_meal_log["solt"]

        return FoodLog(**nutritions)

    def _scrape_food_log(self, html: str) -> dict:
        """
        Scrape food log data from HTML content.
        Args:
            html (str): HTML content of the food log page.
        Returns:
            FoodLog: Parsed food log data.
        """
        soup = BeautifulSoup(html, "html.parser")
        nutritions = {"date": ""}
        nutritions_ele = soup.find_all("li", class_="line_left")
        for nutrition_ele in nutritions_ele:
            nutrition_name = nutrition_ele.find("li", class_="title").text.strip()
            nutrition_value = nutrition_ele.find("li", class_="val").text.strip()

            if nutrition_name in NUTRITIONS:
                nutritions[NUTRITIONS[nutrition_name]] = remove_unit(nutrition_value)

        return nutritions

from typing import Optional

import requests
from requests.exceptions import RequestException


from asken import Asken, FoodLog
from fitbit import Fitbit
from const import MEAL_TYPES
from models.fitbit import CreateFoodLogParams, GetFoodLogResponse
from utils import get_logger


logger = get_logger(__name__)


def safe_api_call(api_name=""):
    """
    A wrapper to safely call API functions and handle exceptions.
    Args:
        func (callable): The API function to call.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.
    Returns:
        The result of the API call or None if an error occurs.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RequestException as e:
                logger.error(
                    f"{api_name} API request error: {e} (func={func.__name__}, args={args}, kwargs={kwargs})"
                )
                return None
            except Exception as e:
                logger.error(
                    f"Unexpected error in {api_name}: {e} (func={func.__name__}, args={args}, kwargs={kwargs})"
                )
                return None

        return wrapper

    return decorator


class AskenFitbitSync:
    def __init__(self, asken: Asken, fitbit: Fitbit):
        self._asken = asken
        self._fitbit = fitbit

    @safe_api_call("Asken")
    def fetch_asken_food_log(self, date: str, meal_type_id: int) -> FoodLog:
        """
        Fetch food log from Asken for a specific date and meal type.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
            meal_type_id (int): Meal type ID (1: 朝食, 2: 昼食, 3: 夕食, 4: 間食).
        Returns:
            FoodLog: Parsed food log data.
        """
        return self._asken.fetch_food_log(date, meal_type_id)

    @safe_api_call("Fitbit")
    def fetch_fitbit_food_log(self, date: str) -> GetFoodLogResponse:
        """
        Fetch food log from Fitbit for a specific date.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
        Returns:
            GetFoodLogResponse: Parsed food log data.
        """
        return self._fitbit.fetch_food_log(date)

    @safe_api_call("Fitbit")
    def delete_fitbit_food_log(self, food_log_id: int) -> requests.Response:
        """
        Delete a food log from Fitbit by its ID.
        Args:
            food_log_id (int): The ID of the food log to delete.
        """
        return self._fitbit.delete_food_log(food_log_id)

    @safe_api_call("Fitbit")
    def create_fitbit_food_log(self, params: CreateFoodLogParams) -> dict:
        """
        Create a food log in Fitbit.
        Args:
            params (CreateFoodLogParams): Parameters for creating the food log.
        """
        return self._fitbit.create_food_log(params)

    def sync_food_logs(
        self, date: str, meal_type_id_list: list[int] = [1, 2, 3, 4]
    ) -> None:
        """
        Sync food logs for a specific date and meal type IDs.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
            meal_type_id_list (list[int]): List of meal type IDs to sync. Defaults to [1, 2, 3, 4] (朝食, 昼食, 夕食, 間食).
        """

        food_logs: GetFoodLogResponse = self._fitbit.fetch_food_log(date)
        if not food_logs:
            return

        for meal_type_id in meal_type_id_list:
            meal: FoodLog = self._asken.fetch_food_log(date, meal_type_id)
            if not meal or not meal.logged:
                logger.info(
                    f"No food log found for date {date} and meal type {meal_type_id}."
                )
                continue

            is_registered = False
            for food_log in food_logs.foods:
                if (
                    food_log.loggedFood.mealTypeId
                    == MEAL_TYPES[meal_type_id]["fitbit_id"]
                ):
                    registered_log = food_log.loggedFood
                    food_log_id = food_log.logId
                    is_registered = True

            # updateではPFC情報が更新できないため、削除して再登録
            if is_registered:
                if registered_log.calories != meal.calories:
                    logger.info(f"Delete {MEAL_TYPES[meal_type_id]['name']} on {date}")
                    res = self._fitbit.delete_food_log(food_log_id)
                    if not res:
                        continue
                else:
                    logger.info(
                        f"Already registered {MEAL_TYPES[meal_type_id]['name']} on {date}"
                    )
                    continue

            params = CreateFoodLogParams(
                **{
                    "foodName": MEAL_TYPES[meal_type_id]["name"],
                    "mealTypeId": MEAL_TYPES[meal_type_id]["fitbit_id"],
                    "unitId": 304,  # 単位: 食分
                    "amount": 1,
                    "date": date,
                    "calories": meal.calories,
                    "protein": meal.protein,
                    "totalFat": meal.fat,
                    "totalCarbohydrate": meal.carbs,
                }
            )

            res = self._fitbit.create_food_log(params)
            if not res:
                continue

            logger.info(f"Create {MEAL_TYPES[meal_type_id]['name']} on {date}")

    def sync_weight(
        self, date: str, weight: float, body_fat: Optional[float] = None
    ) -> None:
        """
        Sync weight and body fat percentage to Fitbit.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
            weight (float): Weight in kg.
            body_fat (Optional[float]): Body fat percentage. Defaults to None. if not provided, body fat will not be synced.
        """
        pass

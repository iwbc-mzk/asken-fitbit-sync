from typing import Optional

from asken import Asken, FoodLog
from fitbit import Fitbit
from const import MEAL_TYPES
from models.fitbit import CreateFoodLogParams
from utils import get_logger


logger = get_logger(__name__)


class AskenFitbitSync:
    def __init__(self, asken: Asken, fitbit: Fitbit):
        self._asken = asken
        self._fitbit = fitbit

    def sync_food_logs(
        self, date: str, meal_type_id_list: list[int] = [1, 2, 3, 4]
    ) -> None:
        """
        Sync food logs for a specific date and meal type IDs.
        Args:
            date (str): Date in the format 'YYYY-MM-DD'.
            meal_type_id_list (list[int]): List of meal type IDs to sync. Defaults to [1, 2, 3, 4] (朝食, 昼食, 夕食, 間食).
        """

        food_logs = self._fitbit.fetch_food_log(date)

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
                    self._fitbit.delete_food_log(food_log_id)
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

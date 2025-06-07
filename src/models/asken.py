from decimal import Decimal

from pydantic import BaseModel


class FoodLog(BaseModel):
    date: str
    meal_type_id: int
    calories: float | Decimal = 0.0  # カロリー(kcal)
    protein: float | Decimal = 0.0  # タンパク質(g)
    fat: float | Decimal = 0.0  # 脂質(g)
    carbs: float | Decimal = 0.0  # 炭水化物(g)
    calcium: float | Decimal = 0.0  # カルシウム(mg)
    magnesium: float | Decimal = 0.0  # マグネシウム(mg)
    iron: float | Decimal = 0.0  # 鉄分(mg)
    zinc: float | Decimal = 0.0  # 亜鉛(mg)
    vitamin_a: float | Decimal = 0.0  # ビタミンA(μg)
    vitamin_d: float | Decimal = 0.0  # ビタミンD(μg)
    vitamin_b1: float | Decimal = 0.0  # ビタミンB1(mg)
    vitamin_b2: float | Decimal = 0.0  # ビタミンB2(mg)
    vitamin_b6: float | Decimal = 0.0  # ビタミンB6(mg)
    vitamin_c: float | Decimal = 0.0  # ビタミンC(mg)
    fiber: float | Decimal = 0.0  # 食物繊維(g)
    saturatedFat: float | Decimal = 0.0  # 飽和脂肪酸(g)
    solt: float | Decimal = 0.0  # 食塩相当量(g)
    logged: bool = False  # 食事記録が登録済かどうか

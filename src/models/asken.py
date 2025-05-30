from pydantic import BaseModel


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

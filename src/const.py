from typing import Any


UNITS: dict[str, dict[str, int]] = {
    "mg": {"word_cnt": 2},
    "μg": {"word_cnt": 2},
    "kg": {"word_cnt": 2},
    "g": {"word_cnt": 1},
    "kcal": {"word_cnt": 4},
    "cal": {"word_cnt": 3},
}

MEAL_TYPES: dict[int, dict[str, Any]] = {
    1: {
        "name": "朝食（あすけん）",
        "asken_id": 3,
        "fitbit_id": 1,
    },
    2: {
        "name": "昼食（あすけん）",
        "asken_id": 4,
        "fitbit_id": 3,
    },
    3: {
        "name": "夕食（あすけん）",
        "asken_id": 5,
        "fitbit_id": 5,
    },
    4: {
        "name": "間食（あすけん）",
        "asken_id": 6,
        "fitbit_id": 7,
    },
}

DAILY_MEAL_TYPE_ID_LIST: list[int] = [1, 2, 3, 4]  # 朝食, 昼食, 夕食, 間食


NUTRITIONS: dict[str, str] = {
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

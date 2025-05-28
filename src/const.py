FITBIT_API_URL = "https://api.fitbit.com"

UNITS = {
    "mg": {"word_cnt": 2},
    "μg": {"word_cnt": 2},
    "kg": {"word_cnt": 2},
    "g": {"word_cnt": 1},
    "kcal": {"word_cnt": 4},
    "cal": {"word_cnt": 3},
}

MEAL_TYPES = {
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

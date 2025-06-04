GET_FOOD_LOG_RESPONSE_JSON = {
    "foods": [
        {
            "isFavorite": True,
            "logDate": "2019-03-21",
            "logId": 17406206369,
            "loggedFood": {
                "accessLevel": "PUBLIC",
                "amount": 1,
                "brand": "Subway",
                "calories": 280,
                "foodId": 14022778,
                "locale": "en_US",
                "mealTypeId": 3,
                "name": "6 inch Turkey Breast",
                "unit": {"id": 296, "name": "sandwich", "plural": "sandwiches"},
                "units": [296, 226, 180, 147, 389],
            },
            "nutritionalValues": {
                "calories": 280,
                "carbs": 46,
                "fat": 3.5,
                "fiber": 5,
                "protein": 18,
                "sodium": 760,
            },
        }
    ],
    "goals": {"calories": 2910},
    "summary": {
        "calories": 280,
        "carbs": 46,
        "fat": 3.5,
        "fiber": 5,
        "protein": 18,
        "sodium": 760,
        "water": 0,
    },
}

CREATE_FOOD_LOG_PARAMS_JSON = {
    "mealTypeId": 1,
    "unitId": 304,
    "amount": 1,
    "date": "2024-01-01",
    "calories": 1000,
    "totalFat": 100,
    "totalCarbohydrate": 200,
    "protein": 60,
}

CREATE_FOOD_LOG_RESPONSE_JSON = {
    "foodDay": {
        "date": "2019-03-21",
        "summary": {
            "calories": 1224,
            "carbs": 165.85,
            "fat": 48.13,
            "fiber": 17.75,
            "protein": 30.75,
            "sodium": 1588.75,
            "water": 1892.7099609375,
        },
    },
    "foodLog": {
        "isFavorite": True,
        "logDate": "2019-03-21",
        "logId": 17406014466,
        "loggedFood": {
            "accessLevel": "PUBLIC",
            "amount": 2.55,
            "brand": "",
            "calories": 944,
            "foodId": 82294,
            "locale": "en_US",
            "mealTypeId": 3,
            "name": "Chips",
            "unit": {"id": 304, "name": "serving", "plural": "servings"},
            "units": [304, 226, 180, 147, 389],
        },
        "nutritionalValues": {
            "calories": 944,
            "carbs": 119.85,
            "fat": 44.63,
            "fiber": 12.75,
            "protein": 12.75,
            "sodium": 828.75,
        },
    },
}

UPDATE_FOOD_LOG_PARAMS_JSON = {
    "mealTypeId": 1,
    "unitid": 304,  # 単位: 食分
    "amount": 1,
    "calories": 1500,
}

UPDATE_FOOD_LOG_RESPONSE_JSON = {
    "foodLog": {
        "isFavorite": False,
        "logDate": "2020-06-10",
        "logId": 22100146659,
        "loggedFood": {
            "accessLevel": "PUBLIC",
            "amount": 1,
            "brand": "",
            "calories": 130,
            "foodId": 81409,
            "locale": "en_US",
            "mealTypeId": 1,
            "name": "Apple",
            "unit": {"id": 179, "name": "large", "plural": "larges"},
            "units": [204, 179, 226, 180, 147, 389],
        },
        "nutritionalValues": {
            "calories": 130,
            "carbs": 35.75,
            "fat": 0,
            "fiber": 8.13,
            "protein": 0,
            "sodium": 0,
        },
    }
}

REFRESH_ACCESS_TOKEN_RESPONSE = {
    "access_token": "eyJhbGciOiJIUzI1...",
    "expires_in": 28800,
    "refresh_token": "c643a63c072f0f05478e9d18b991db80ef6061e...",
    "token_type": "Bearer",
    "user_id": "GGNJL9",
}

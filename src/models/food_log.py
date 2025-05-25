from typing import Optional
from pydantic import BaseModel


class Unit(BaseModel):
    id: int
    name: str
    plural: str


class NutritionalValues(BaseModel):
    calories: float
    carbs: float
    fat: float
    fiber: float
    protein: float
    sodium: float


class LoggedFood(BaseModel):
    accessLevel: str
    amount: int
    brand: str
    calories: float
    foodId: int
    foodName: Optional[str] = None
    mealTypeId: int
    name: str
    unit: Unit
    units: list[int]


class Food(BaseModel):
    isFavorite: bool
    logDate: str
    logId: int
    loggedFood: LoggedFood
    nutritionalValues: NutritionalValues


class FoodsLog(BaseModel):
    foods: list[Food]
    goals: dict
    summary: dict


class Goal(BaseModel):
    calories: float


class Summary(BaseModel):
    calories: float
    carbs: float
    fat: float
    fiber: float
    protein: float
    sodium: float
    water: float


class FoodLogResponse(BaseModel):
    foods: list[Food]
    goals: Goal
    summary: Summary

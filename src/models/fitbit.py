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


class GetFoodLogResponse(BaseModel):
    foods: list[Food]
    goals: Optional[Goal] = None
    summary: Summary


class UpdateFoodLogParams(BaseModel):
    mealTypeId: int
    unitid: int = 304  # 単位: 食分
    amount: int
    calories: float


class CreateFoodLogParams(BaseModel):
    foodId: Optional[int] = None
    foodName: Optional[str] = None
    mealTypeId: int
    unitId: int
    amount: int
    date: str
    favorite: Optional[bool] = None
    brandName: Optional[str] = None
    calories: Optional[int] = None
    caloriesFromFat: Optional[int] = None
    totalFat: Optional[float] = None  # 脂質(g)
    transFat: Optional[float] = None  # トランス脂肪酸(g)
    saturatedFat: Optional[float] = None  # 飽和脂肪酸(g)
    cholesterol: Optional[float] = None  # コレステロール(mg)
    sodium: Optional[float] = None  # ナトリウム(mg)
    potassium: Optional[float] = None  # カリウム(mg)
    totalCarbohydrate: Optional[float] = None  # 炭水化物(g)
    dietaryFiber: Optional[int] = None  # 食物繊維(g)
    sugars: Optional[float] = None  # 糖質(g)
    protein: Optional[float] = None  # タンパク質(g)
    vitaminA: Optional[float] = None  # ビタミンA(IU)
    vitaminB6: Optional[float] = None  # ビタミンB6
    vitaminB12: Optional[float] = None  # ビタミンB12
    vitaminC: Optional[float] = None  # ビタミンC(mg)
    vitaminD: Optional[float] = None  # ビタミンD(IU)
    vitaminE: Optional[float] = None  # ビタミンE(IU)
    biotin: Optional[float] = None  # ビオチン(mg)
    folicAcid: Optional[float] = None  # 葉酸(mg)
    niacin: Optional[float] = None  # ナイアシン(mg)
    pantothenicAcid: Optional[float] = None  # パントテン酸(mg)
    riboflavin: Optional[float] = None  # リボフラビン(mg)
    thiamin: Optional[float] = None  # チアミン(mg)
    calcium: Optional[float] = None  # カルシウム(g)
    copper: Optional[float] = None  # 銅(g)
    iron: Optional[float] = None  # 鉄分(mg)
    magnesium: Optional[float] = None  # マグネシウム(mg)
    phosphorus: Optional[float] = None  # リン(mg)
    iodine: Optional[float] = None  # ヨウ素(mcg)
    zinc: Optional[float] = None  # 亜鉛(mg)

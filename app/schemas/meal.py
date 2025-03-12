from typing import Optional
from datetime import date
from pydantic import BaseModel

class MealBase(BaseModel):
    idMembro: int
    idCargo: int
    dataPosse: date
    dataLimitePosse: Optional[date] = None

class MealCreate(MealBase):
    pass

class MealUpdate(MealBase):
    pass

class Meal(MealBase):
    idMeal: int

    class Config:
        orm_mode = True
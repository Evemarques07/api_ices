from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import meal as meal_crud
from app.schemas import meal as meal_schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=meal_schemas.Meal)
def create_meal(meal: meal_schemas.MealCreate, db: Session = Depends(get_db)):
    return meal_crud.create_meal(db=db, meal=meal)

@router.get("/", response_model=List[meal_schemas.Meal])
def read_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meals_list = meal_crud.get_meals(db, skip=skip, limit=limit)
    return meals_list

@router.get("/{meal_id}", response_model=meal_schemas.Meal)
def read_meal(meal_id: int, db: Session = Depends(get_db)):
    db_meal = meal_crud.get_meal(db, meal_id=meal_id)
    if db_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return db_meal

@router.put("/{meal_id}", response_model=meal_schemas.Meal)
def update_meal(meal_id: int, meal: meal_schemas.MealUpdate, db: Session = Depends(get_db)):
    db_meal = meal_crud.update_meal(db, meal_id=meal_id, meal_update=meal)
    if db_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return db_meal

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    db_meal = meal_crud.delete_meal(db, meal_id=meal_id)
    if db_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return {"ok": True}
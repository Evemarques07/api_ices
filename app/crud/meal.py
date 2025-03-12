from sqlalchemy.orm import Session
from app.models import meal
from app.schemas import meal as meal_schemas

def get_meal(db: Session, meal_id: int):
    return db.query(meal.Meal).filter(meal.Meal.idMeal == meal_id).first()

def get_meals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(meal.Meal).offset(skip).limit(limit).all()

def create_meal(db: Session, meal: meal_schemas.MealCreate):
    db_meal = meal.Meal(**meal.dict())
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def update_meal(db: Session, meal_id: int, meal_update: meal_schemas.MealUpdate):
    db_meal = get_meal(db, meal_id)
    if db_meal:
        for key, value in meal_update.dict(exclude_unset=True).items():
            setattr(db_meal, key, value)
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
    return db_meal

def delete_meal(db: Session, meal_id: int):
    db_meal = get_meal(db, meal_id)
    if db_meal:
        db.delete(db_meal)
        db.commit()
    return db_meal
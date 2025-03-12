from sqlalchemy.orm import Session
from app.models import cargos
from app.schemas import cargos as cargos_schemas

def get_cargo(db: Session, cargo_id: int):
    return db.query(cargos.Cargo).filter(cargos.Cargo.idCargo == cargo_id).first()

def get_cargos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(cargos.Cargo).offset(skip).limit(limit).all()

def create_cargo(db: Session, cargo: cargos_schemas.CargoCreate):
    db_cargo = cargos.Cargo(**cargo.dict())
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo

def update_cargo(db: Session, cargo_id: int, cargo_update: cargos_schemas.CargoUpdate):
    db_cargo = get_cargo(db, cargo_id)
    if db_cargo:
        for key, value in cargo_update.dict(exclude_unset=True).items():
            setattr(db_cargo, key, value)
        db.add(db_cargo)
        db.commit()
        db.refresh(db_cargo)
    return db_cargo

def delete_cargo(db: Session, cargo_id: int):
    db_cargo = get_cargo(db, cargo_id)
    if db_cargo:
        db.delete(db_cargo)
        db.commit()
    return db_cargo
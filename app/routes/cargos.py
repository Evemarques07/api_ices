from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import cargos as cargos_crud
from app.schemas import cargos as cargos_schemas
from database import get_db
from app.core.security import check_senior_presidente_secretario

router = APIRouter()

@router.post("/", response_model=cargos_schemas.Cargo, dependencies=[Depends(check_senior_presidente_secretario)])
def create_cargo(cargo: cargos_schemas.CargoCreate, db: Session = Depends(get_db)):
    return cargos_crud.create_cargo(db=db, cargo=cargo)

@router.get("/", response_model=List[cargos_schemas.Cargo])
def read_cargos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cargos_list = cargos_crud.get_cargos(db, skip=skip, limit=limit)
    return cargos_list

@router.get("/{cargo_id}", response_model=cargos_schemas.Cargo)
def read_cargo(cargo_id: int, db: Session = Depends(get_db)):
    db_cargo = cargos_crud.get_cargo(db, cargo_id=cargo_id)
    if db_cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return db_cargo

@router.put("/{cargo_id}", response_model=cargos_schemas.Cargo, dependencies=[Depends(check_senior_presidente_secretario)])
def update_cargo(cargo_id: int, cargo: cargos_schemas.CargoUpdate, db: Session = Depends(get_db)):
    db_cargo = cargos_crud.update_cargo(db, cargo_id=cargo_id, cargo_update=cargo)
    if db_cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return db_cargo

@router.delete("/{cargo_id}", dependencies=[Depends(check_senior_presidente_secretario)])
def delete_cargo(cargo_id: int, db: Session = Depends(get_db)):
    db_cargo = cargos_crud.delete_cargo(db, cargo_id=cargo_id)
    if db_cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return {"ok": True}
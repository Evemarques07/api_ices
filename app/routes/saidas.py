from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import saidas as saidas_crud
from app.schemas import saidas as saidas_schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=saidas_schemas.Saida)
def create_saida(saida: saidas_schemas.SaidaCreate, db: Session = Depends(get_db)):
    return saidas_crud.create_saida(db=db, saida=saida)

@router.get("/", response_model=List[saidas_schemas.Saida])
def read_saidas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    saidas_list = saidas_crud.get_saidas(db, skip=skip, limit=limit)
    return saidas_list

@router.get("/{saida_id}", response_model=saidas_schemas.Saida)
def read_saida(saida_id: int, db: Session = Depends(get_db)):
    db_saida = saidas_crud.get_saida(db, saida_id=saida_id)
    if db_saida is None:
        raise HTTPException(status_code=404, detail="Saida not found")
    return db_saida

@router.put("/{saida_id}", response_model=saidas_schemas.Saida)
def update_saida(saida_id: int, saida: saidas_schemas.SaidaUpdate, db: Session = Depends(get_db)):
    db_saida = saidas_crud.update_saida(db, saida_id=saida_id, saida_update=saida)
    if db_saida is None:
        raise HTTPException(status_code=404, detail="Saida not found")
    return db_saida

@router.delete("/{saida_id}")
def delete_saida(saida_id: int, db: Session = Depends(get_db)):
    db_saida = saidas_crud.delete_saida(db, saida_id=saida_id)
    if db_saida is None:
        raise HTTPException(status_code=404, detail="Saida not found")
    return {"ok": True}
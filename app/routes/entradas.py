from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import entradas as entradas_crud
from app.schemas import entradas as entradas_schemas
from database import get_db
from app.core.security import check_senior_presidente_tesoureiro_patrimonio, get_current_user
from app.models import entradas

router = APIRouter()

@router.post("/", response_model=entradas_schemas.Entrada, dependencies=[Depends(check_senior_presidente_tesoureiro_patrimonio)])
def create_entrada(entrada: entradas_schemas.EntradaCreate, db: Session = Depends(get_db)):
    return entradas_crud.create_entrada(db=db, entrada=entrada)

@router.get("/", response_model=List[entradas_schemas.Entrada], dependencies=[Depends(check_senior_presidente_tesoureiro_patrimonio)])
def read_entradas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entradas_list = entradas_crud.get_entradas(db, skip=skip, limit=limit)
    return entradas_list

@router.get("/{entrada_id}", response_model=entradas_schemas.Entrada, dependencies=[Depends(check_senior_presidente_tesoureiro_patrimonio)])
def read_entrada(entrada_id: int, db: Session = Depends(get_db)):
    db_entrada = entradas_crud.get_entrada(db, entrada_id=entrada_id)
    if db_entrada is None:
        raise HTTPException(status_code=404, detail="Entrada not found")
    return db_entrada

@router.put("/{entrada_id}", response_model=entradas_schemas.Entrada, dependencies=[Depends(check_senior_presidente_tesoureiro_patrimonio)])
def update_entrada(entrada_id: int, entrada: entradas_schemas.EntradaUpdate, db: Session = Depends(get_db)):
    db_entrada = entradas_crud.update_entrada(db, entrada_id=entrada_id, entrada_update=entrada)
    if db_entrada is None:
        raise HTTPException(status_code=404, detail="Entrada not found")
    return db_entrada

@router.delete("/{entrada_id}", dependencies=[Depends(check_senior_presidente_tesoureiro_patrimonio)])
def delete_entrada(entrada_id: int, db: Session = Depends(get_db)):
    db_entrada = entradas_crud.delete_entrada(db, entrada_id=entrada_id)
    if db_entrada is None:
        raise HTTPException(status_code=404, detail="Entrada not found")
    return {"ok": True}

@router.get("/me/", response_model=List[entradas_schemas.Entrada])
def read_entradas_me(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Lista as entradas do usuário logado.
    """
    id_membro = current_user["idMembro"]
    entradas_list = db.query(entradas.Entrada).filter(entradas.Entrada.idMembro == id_membro).offset(skip).limit(limit).all()
    return entradas_list
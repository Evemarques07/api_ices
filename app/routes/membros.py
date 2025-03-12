from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import membros as membros_crud
from app.schemas import membros as membros_schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=membros_schemas.Membro)
def create_membro(membro: membros_schemas.MembroCreate, db: Session = Depends(get_db)):
    db_membro = membros_crud.get_membro_by_cpf(db, cpf=membro.cpf)
    if db_membro:
        raise HTTPException(status_code=400, detail="CPF already registered")
    return membros_crud.create_membro(db=db, membro=membro)

@router.get("/", response_model=List[membros_schemas.Membro])
def read_membros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    membros = membros_crud.get_membros(db, skip=skip, limit=limit)
    return membros

@router.get("/{membro_id}", response_model=membros_schemas.Membro)
def read_membro(membro_id: int, db: Session = Depends(get_db)):
    db_membro = membros_crud.get_membro(db, membro_id=membro_id)
    if db_membro is None:
        raise HTTPException(status_code=404, detail="Membro not found")
    return db_membro

@router.put("/{membro_id}", response_model=membros_schemas.Membro)
def update_membro(membro_id: int, membro: membros_schemas.MembroUpdate, db: Session = Depends(get_db)):
    db_membro = membros_crud.update_membro(db, membro_id=membro_id, membro_update=membro)
    if db_membro is None:
        raise HTTPException(status_code=404, detail="Membro not found")
    return db_membro

@router.delete("/{membro_id}")
def delete_membro(membro_id: int, db: Session = Depends(get_db)):
    db_membro = membros_crud.delete_membro(db, membro_id=membro_id)
    if db_membro is None:
        raise HTTPException(status_code=404, detail="Membro not found")
    return {"ok": True}
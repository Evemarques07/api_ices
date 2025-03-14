from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import avisos as avisos_crud
from app.schemas import avisos as avisos_schemas
from database import get_db
from app.core.security import check_allowed_cargos  # Ou outra dependência de segurança
from app.models import avisos

router = APIRouter()

@router.post("/", response_model=avisos_schemas.Aviso, dependencies=[Depends(check_allowed_cargos)])
def create_aviso(aviso: avisos_schemas.AvisoCreate, db: Session = Depends(get_db)):
    return avisos_crud.create_aviso(db=db, aviso=aviso)

@router.get("/", response_model=List[avisos_schemas.Aviso], dependencies=[Depends(check_allowed_cargos)])
def read_avisos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    avisos_list = avisos_crud.get_avisos(db, skip=skip, limit=limit)
    return avisos_list

@router.get("/{aviso_id}", response_model=avisos_schemas.Aviso, dependencies=[Depends(check_allowed_cargos)])
def read_aviso(aviso_id: int, db: Session = Depends(get_db)):
    db_aviso = avisos_crud.get_aviso(db, aviso_id=aviso_id)
    if db_aviso is None:
        raise HTTPException(status_code=404, detail="Aviso not found")
    return db_aviso

@router.put("/{aviso_id}", response_model=avisos_schemas.Aviso, dependencies=[Depends(check_allowed_cargos)])
def update_aviso(aviso_id: int, aviso: avisos_schemas.AvisoUpdate, db: Session = Depends(get_db)):
    db_aviso = avisos_crud.update_aviso(db, aviso_id=aviso_id, aviso_update=aviso)
    if db_aviso is None:
        raise HTTPException(status_code=404, detail="Aviso not found")
    return db_aviso

@router.delete("/{aviso_id}", dependencies=[Depends(check_allowed_cargos)])
def delete_aviso(aviso_id: int, db: Session = Depends(get_db)):
    db_aviso = avisos_crud.delete_aviso(db, aviso_id=aviso_id)
    if db_aviso is None:
        raise HTTPException(status_code=404, detail="Aviso not found")
    return {"ok": True}

@router.get("/ativos/", response_model=List[avisos_schemas.Aviso], dependencies=[Depends(check_allowed_cargos)])
def read_avisos_ativos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna apenas os avisos com status ativo (status=True).
    """
    avisos_list = db.query(avisos.Aviso).filter(avisos.Aviso.status == True).offset(skip).limit(limit).all()
    return avisos_list
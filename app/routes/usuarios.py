from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import usuarios as usuarios_crud
from app.crud import membros as membros_crud
from app.schemas import usuarios as usuarios_schemas
from database import get_db
from app.core.security import check_senior_presidente_secretario, get_current_user

router = APIRouter()

@router.post("/", response_model=usuarios_schemas.Usuario, dependencies=[Depends(check_senior_presidente_secretario)])
def create_usuario(usuario: usuarios_schemas.UsuarioCreate, id_membro: int, db: Session = Depends(get_db)):
    db_usuario = usuarios_crud.get_usuario_by_login(db, login=usuario.login)
    db_membro = membros_crud.get_membro(db, membro_id=id_membro)

    if not db_membro:
        raise HTTPException(status_code=404, detail="Membro not found")

    if db_usuario:
        raise HTTPException(status_code=400, detail="Login already registered")
    return usuarios_crud.create_usuario(db=db, usuario=usuario, id_membro=id_membro)

@router.get("/", response_model=List[usuarios_schemas.Usuario], dependencies=[Depends(check_senior_presidente_secretario)])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios_list = usuarios_crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios_list

@router.get("/{usuario_id}", response_model=usuarios_schemas.Usuario, dependencies=[Depends(check_senior_presidente_secretario)])
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = usuarios_crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

@router.put("/{usuario_id}", response_model=usuarios_schemas.Usuario, dependencies=[Depends(check_senior_presidente_secretario)])
def update_usuario(usuario_id: int, usuario: usuarios_schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = usuarios_crud.update_usuario(db, usuario_id=usuario_id, usuario_update=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

@router.patch("/{usuario_id}", response_model=usuarios_schemas.Usuario)
def update_usuario_partial(usuario_id: int, usuario: usuarios_schemas.UsuarioUpdatePartial, db: Session = Depends(get_db)):
    db_usuario = usuarios_crud.update_usuario_partial(db, usuario_id=usuario_id, usuario_update=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

@router.delete("/{usuario_id}", dependencies=[Depends(check_senior_presidente_secretario)])
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = usuarios_crud.delete_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return {"ok": True}
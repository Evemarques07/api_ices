from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.crud import usuarios as usuarios_crud
from app.crud import membros as membros_crud
from app.schemas import usuarios as usuarios_schemas
from database import get_db

router = APIRouter()

@router.post("/token", response_model=usuarios_schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = usuarios_crud.get_usuario_by_login(db, login=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    membro = membros_crud.get_membro(db, user.idMembro)
    cargo = "membro"

    if membro:
        for m in membro.meals:
            cargo = m.cargo.nomeCargo

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    subject = {
            "idMembro": user.idMembro,
            "nomeCompleto": membro.nomeCompleto if membro else None,
            "cpf": membro.cpf if membro else None,
            "cargo": cargo
        }
    access_token = security.create_access_token(
        subject=subject, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
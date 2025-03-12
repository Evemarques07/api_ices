from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from decouple import config
from sqlalchemy.orm import Session
from database import get_db

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_membro: int = payload.get("idMembro")
        nome_completo: str = payload.get("nomeCompleto")
        cpf: str = payload.get("cpf")
        cargo: str = payload.get("cargo")

        if id_membro is None or nome_completo is None or cpf is None or cargo is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = {"idMembro": id_membro, "nomeCompleto": nome_completo, "cpf": cpf, "cargo": cargo}
    return user

def check_senior_presidente_secretario(current_user: dict = Depends(get_current_user)):
    allowed_cargos = ["Senior", "Presidente", "Secretário", "Vice-secretário"]
    if current_user["cargo"] not in allowed_cargos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )
    return current_user

def check_senior_presidente_tesoureiro_patrimonio(current_user: dict = Depends(get_current_user)):
    allowed_cargos = ["Senior", "Presidente", "Tesoureiro", "Vice-tesoureiro", "Diretor de patrimonio"]
    if current_user["cargo"] not in allowed_cargos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )
    return current_user


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = subject
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
from typing import Optional
from datetime import date
from pydantic import BaseModel

class MembroBase(BaseModel):
    nomeCompleto: str
    cpf: str
    dataNascimento: Optional[date] = None
    telefone: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    naturalidade: Optional[str] = None
    dataBatismo: Optional[date] = None
    dataInclusao: Optional[date] = None
    dataExclusao: Optional[date] = None
    status: Optional[bool] = True

class MembroCreate(MembroBase):
    pass

class MembroUpdate(MembroBase):
    pass

class Membro(MembroBase):
    idMembro: int

    class Config:
        orm_mode = True
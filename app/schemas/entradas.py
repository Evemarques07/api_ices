from typing import Optional
from datetime import date
from pydantic import BaseModel
from enum import Enum

class TipoEntrada(str, Enum):
    Dizimos = "Dizimos"
    Ofertas = "Ofertas"
    Campanhas = "Campanhas"
    Eventos = "Eventos"
    Alugueis = "Alugueis"
    Doacoes = "Doacoes"

class EntradaBase(BaseModel):
    tipo: TipoEntrada
    idMembro: Optional[int] = None
    descricao: Optional[str] = None
    dataRegistro: date
    valor: float
    observacao: Optional[str] = None

class EntradaCreate(EntradaBase):
    pass

class EntradaUpdate(EntradaBase):
    pass

class Entrada(EntradaBase):
    idEntrada: int

    class Config:
        orm_mode = True
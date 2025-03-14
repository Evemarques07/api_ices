from typing import Optional
from datetime import date
from pydantic import BaseModel

class AvisoBase(BaseModel):
    idMembro: int
    descricao: str
    dataEvento: Optional[date] = None
    status: Optional[bool] = True

class AvisoCreate(AvisoBase):
    pass

class AvisoUpdate(AvisoBase):
    pass

class Aviso(AvisoBase):
    idAviso: int

    class Config:
        orm_mode = True
from typing import Optional
from pydantic import BaseModel

class CargoBase(BaseModel):
    nomeCargo: Optional[str] = "membro"
    descricao: Optional[str] = None

class CargoCreate(CargoBase):
    pass

class CargoUpdate(CargoBase):
    pass

class Cargo(CargoBase):
    idCargo: int

    class Config:
        orm_mode = True
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    login: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    idUser: int
    idMembro: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    idMembro: int | None = None
    nomeCompleto: str | None = None
    cpf: str | None = None
    cargo: str | None = None
from typing import Optional
from datetime import date
from pydantic import BaseModel
from enum import Enum

class TipoSaida(str, Enum):
    Folha_Pagamento = "Folha_Pagamento"
    Agua_Luz = "Agua_Luz"
    Aluguel_Imovel = "Aluguel_Imovel"
    Manutencao = "Manutencao"
    Aquisicao_bens = "Aquisicao_bens"
    Eventos_Custos = "Eventos_Custos"
    Ajuda_Social = "Ajuda_Social"
    Materiais_Culto = "Materiais_Culto"
    Impostos_Taxas = "Impostos_Taxas"

class SaidaBase(BaseModel):
    tipo: TipoSaida
    idMembro: Optional[int] = None
    descricao: Optional[str] = None
    dataRegistro: date
    valor: float
    observacao: Optional[str] = None

class SaidaCreate(SaidaBase):
    pass

class SaidaUpdate(SaidaBase):
    pass

class Saida(SaidaBase):
    idSaida: int

    class Config:
        orm_mode = True
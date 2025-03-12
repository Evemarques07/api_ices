from typing import Optional
from datetime import date   
from pydantic import BaseModel
from enum import Enum

# Alinhamento com o Enum do SQLAlchemy
class TipoEntrada(str, Enum):
    Dizimos = "Dizimos"
    Ofertas = "Ofertas"
    Ofertas_Missionarias = "Ofertas_Missionarias"
    Campanhas = "Campanhas"
    Eventos = "Eventos"
    Venda_Materiais = "Venda_Materiais"
    Doacoes_Empresas = "Doacoes_Empresas"
    Parcerias_Ongs = "Parcerias_Ongs"
    Apoio_Outras_Igrejas = "Apoio_Outras_Igrejas"
    Investimentos = "Investimentos"

# Classe base para entradas
class EntradaBase(BaseModel):
    tipo: TipoEntrada
    idMembro: Optional[int] = None
    descricao: Optional[str] = None
    dataRegistro: date
    valor: float
    observacao: Optional[str] = None

# Para criação de entradas
class EntradaCreate(EntradaBase):
    pass

# Para atualização de entradas
class EntradaUpdate(EntradaBase):
    pass

# Representação da Entrada (quando carregada do banco de dados)
class Entrada(EntradaBase):
    idEntrada: int

    class Config:
        orm_mode = True

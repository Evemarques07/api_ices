from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoEntrada(enum.Enum):
    Dizimos = "Dizimos"
    Ofertas = "Ofertas"
    Campanhas = "Campanhas"
    Eventos = "Eventos"
    Alugueis = "Alugueis"
    Doacoes = "Doacoes"

class Entrada(Base):
    __tablename__ = "entradas"

    idEntrada = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoEntrada), nullable=False)
    idMembro = Column(Integer, ForeignKey("membros.idMembro"), nullable=True)
    descricao = Column(String(255))
    dataRegistro = Column(Date)
    valor = Column(Numeric(10, 2))
    observacao = Column(String(255))

    # Relacionamentos
    membro = relationship("Membro", back_populates="entradas")
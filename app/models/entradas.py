from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoEntrada(enum.Enum):   
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

    def __repr__(self):
        return f"<Entrada(idEntrada={self.idEntrada}, tipo={self.tipo}, idMembro={self.idMembro})>"

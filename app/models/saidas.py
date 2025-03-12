from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoSaida(enum.Enum):
    Folha_Pagamento = "Folha_Pagamento"
    Agua_Luz = "Agua_Luz"
    Aluguel_Imovel = "Aluguel_Imovel"
    Manutencao = "Manutencao"
    Aquisicao_bens = "Aquisicao_bens"
    Eventos_Custos = "Eventos_Custos"
    Ajuda_Social = "Ajuda_Social"
    Materiais_Culto = "Materiais_Culto"
    Impostos_Taxas = "Impostos_Taxas"


class Saida(Base):
    __tablename__ = "saidas"

    idSaida = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoSaida), nullable=False)
    idMembro = Column(Integer, ForeignKey("membros.idMembro"), nullable=True)
    descricao = Column(String(255))
    dataRegistro = Column(Date)
    valor = Column(Numeric(10, 2))
    observacao = Column(String(255))

    # Relacionamentos
    membro = relationship("Membro", back_populates="saidas")
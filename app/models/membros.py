from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Membro(Base):
    __tablename__ = "membros"

    idMembro = Column(Integer, primary_key=True, index=True)
    nomeCompleto = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    dataNascimento = Column(Date)
    telefone = Column(String(20))
    rua = Column(String(255))
    numero = Column(String(10))
    bairro = Column(String(255))
    cidade = Column(String(255))
    naturalidade = Column(String(255))
    dataBatismo = Column(Date)
    dataInclusao = Column(Date)
    dataExclusao = Column(Date, nullable=True)
    status = Column(Boolean, default=True)

    # Relacionamentos (se houver)
    usuarios = relationship("Usuario", back_populates="membro")
    meals = relationship("Meal", back_populates="membro")  # ou liderancas
    entradas = relationship("Entrada", back_populates="membro")
    saidas = relationship("Saida", back_populates="membro")
    avisos = relationship("Aviso", back_populates="membro")  # Adicione esta linha

    def __repr__(self):
        return f"<Membro(idMembro={self.idMembro}, nomeCompleto='{self.nomeCompleto}')>"
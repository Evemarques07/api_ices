from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    idUser = Column(Integer, primary_key=True, index=True)
    idMembro = Column(Integer, ForeignKey("membros.idMembro"))
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relacionamentos
    membro = relationship("Membro", back_populates="usuarios")
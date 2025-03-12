from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Cargo(Base):
    __tablename__ = "cargos"

    idCargo = Column(Integer, primary_key=True, index=True)
    nomeCargo = Column(String(255), default="membro")
    descricao = Column(String(255))

    # Relacionamentos
    meals = relationship("Meal", back_populates="cargo")
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Meal(Base):
    __tablename__ = "meal"

    idMeal = Column(Integer, primary_key=True, index=True)
    idMembro = Column(Integer, ForeignKey("membros.idMembro"))
    idCargo = Column(Integer, ForeignKey("cargos.idCargo"))
    dataPosse = Column(Date)
    dataLimitePosse = Column(Date)

    # Relacionamentos
    membro = relationship("Membro", back_populates="meals")
    cargo = relationship("Cargo", back_populates="meals")
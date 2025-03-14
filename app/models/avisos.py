from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Aviso(Base):
    __tablename__ = "avisos"

    idAviso = Column(Integer, primary_key=True, index=True)
    idMembro = Column(Integer, ForeignKey("membros.idMembro"))
    descricao = Column(String(255), nullable=False)
    dataEvento = Column(Date)
    status = Column(Boolean, default=True)  # True = ativo, False = inativo

    # Relacionamentos
    membro = relationship("Membro", back_populates="avisos")

    def __repr__(self):
        return f"<Aviso(idAviso={self.idAviso}, idMembro={self.idMembro}, descricao='{self.descricao}', dataEvento={self.dataEvento}, status={self.status})>"
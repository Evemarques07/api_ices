from sqlalchemy.orm import Session
from app.models import saidas
from app.schemas import saidas as saidas_schemas

def get_saida(db: Session, saida_id: int):
    return db.query(saidas.Saida).filter(saidas.Saida.idSaida == saida_id).first()

def get_saidas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(saidas.Saida).offset(skip).limit(limit).all()

def create_saida(db: Session, saida: saidas_schemas.SaidaCreate):
    db_saida = saidas.Saida(**saida.dict())
    db.add(db_saida)
    db.commit()
    db.refresh(db_saida)
    return db_saida

def update_saida(db: Session, saida_id: int, saida_update: saidas_schemas.SaidaUpdate):
    db_saida = get_saida(db, saida_id)
    if db_saida:
        for key, value in saida_update.dict(exclude_unset=True).items():
            setattr(db_saida, key, value)
        db.add(db_saida)
        db.commit()
        db.refresh(db_saida)
    return db_saida

def delete_saida(db: Session, saida_id: int):
    db_saida = get_saida(db, saida_id)
    if db_saida:
        db.delete(db_saida)
        db.commit()
    return db_saida
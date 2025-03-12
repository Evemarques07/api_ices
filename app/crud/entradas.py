from sqlalchemy.orm import Session
from app.models import entradas
from app.schemas import entradas as entradas_schemas

def get_entrada(db: Session, entrada_id: int):
    return db.query(entradas.Entrada).filter(entradas.Entrada.idEntrada == entrada_id).first()

def get_entradas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(entradas.Entrada).offset(skip).limit(limit).all()

def create_entrada(db: Session, entrada: entradas_schemas.EntradaCreate):
    db_entrada = entradas.Entrada(**entrada.dict())
    db.add(db_entrada)
    db.commit()
    db.refresh(db_entrada)
    return db_entrada

def update_entrada(db: Session, entrada_id: int, entrada_update: entradas_schemas.EntradaUpdate):
    db_entrada = get_entrada(db, entrada_id)
    if db_entrada:
        for key, value in entrada_update.dict(exclude_unset=True).items():
            setattr(db_entrada, key, value)
        db.add(db_entrada)
        db.commit()
        db.refresh(db_entrada)
    return db_entrada

def delete_entrada(db: Session, entrada_id: int):
    db_entrada = get_entrada(db, entrada_id)
    if db_entrada:
        db.delete(db_entrada)
        db.commit()
    return db_entrada
from sqlalchemy.orm import Session
from app.models import avisos
from app.schemas import avisos as avisos_schemas

def get_aviso(db: Session, aviso_id: int):
    return db.query(avisos.Aviso).filter(avisos.Aviso.idAviso == aviso_id).first()

def get_avisos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(avisos.Aviso).offset(skip).limit(limit).all()

def create_aviso(db: Session, aviso: avisos_schemas.AvisoCreate):
    db_aviso = avisos.Aviso(**aviso.dict())
    db.add(db_aviso)
    db.commit()
    db.refresh(db_aviso)
    return db_aviso

def update_aviso(db: Session, aviso_id: int, aviso_update: avisos_schemas.AvisoUpdate):
    db_aviso = get_aviso(db, aviso_id)
    if db_aviso:
        for key, value in aviso_update.dict(exclude_unset=True).items():
            setattr(db_aviso, key, value)
        db.add(db_aviso)
        db.commit()
        db.refresh(db_aviso)
    return db_aviso

def delete_aviso(db: Session, aviso_id: int):
    db_aviso = get_aviso(db, aviso_id)
    if db_aviso:
        db.delete(db_aviso)
        db.commit()
    return db_aviso
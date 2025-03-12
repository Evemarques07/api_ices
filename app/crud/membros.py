from sqlalchemy.orm import Session
from app.models import membros
from app.schemas import membros as membros_schemas

def get_membro(db: Session, membro_id: int):
    return db.query(membros.Membro).filter(membros.Membro.idMembro == membro_id).first()

def get_membro_by_cpf(db: Session, cpf: str):
    return db.query(membros.Membro).filter(membros.Membro.cpf == cpf).first()

def get_membros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(membros.Membro).offset(skip).limit(limit).all()

def create_membro(db: Session, membro: membros_schemas.MembroCreate):
    db_membro = membros.Membro(**membro.dict())
    db.add(db_membro)
    db.commit()
    db.refresh(db_membro)
    return db_membro

def update_membro(db: Session, membro_id: int, membro_update: membros_schemas.MembroUpdate):
    db_membro = get_membro(db, membro_id)
    if db_membro:
        for key, value in membro_update.dict(exclude_unset=True).items():
            setattr(db_membro, key, value)
        db.add(db_membro)
        db.commit()
        db.refresh(db_membro)
    return db_membro

def delete_membro(db: Session, membro_id: int):
    db_membro = get_membro(db, membro_id)
    if db_membro:
        db.delete(db_membro)
        db.commit()
    return db_membro
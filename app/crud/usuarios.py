from sqlalchemy.orm import Session
from app.models import usuarios
from app.schemas import usuarios as usuarios_schemas
from app.core.security import get_password_hash

def get_usuario(db: Session, usuario_id: int):
    return db.query(usuarios.Usuario).filter(usuarios.Usuario.idUser == usuario_id).first()

def get_usuario_by_login(db: Session, login: str):
    return db.query(usuarios.Usuario).filter(usuarios.Usuario.login == login).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(usuarios.Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: usuarios_schemas.UsuarioCreate, id_membro: int):
    hashed_password = get_password_hash(usuario.password)
    db_usuario = usuarios.Usuario(login=usuario.login, password=hashed_password, idMembro=id_membro)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario_update: usuarios_schemas.UsuarioCreate):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        hashed_password = get_password_hash(usuario_update.password)
        db_usuario.login = usuario_update.login
        db_usuario.password = hashed_password

        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def update_usuario_partial(db: Session, usuario_id: int, usuario_update: usuarios_schemas.UsuarioUpdatePartial):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        if usuario_update.login is not None:
            db_usuario.login = usuario_update.login
        if usuario_update.password is not None:
            hashed_password = get_password_hash(usuario_update.password)
            db_usuario.password = hashed_password

        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario(db, usuario_id)
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario
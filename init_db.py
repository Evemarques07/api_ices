from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

from app.models import membros, cargos, usuarios, meal, entradas, saidas
from app.core.security import get_password_hash
from database import Base

DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    db = SessionLocal()

    try:
        # 1. Verificar se o cargo "Senior" existe. Se não, criar.
        cargo_senior = db.query(cargos.Cargo).filter(cargos.Cargo.nomeCargo == "Senior").first()
        if not cargo_senior:
            cargo_senior = cargos.Cargo(nomeCargo="Senior", descricao="Cargo com todos os privilegios")
            db.add(cargo_senior)
            db.commit()
            db.refresh(cargo_senior)

        # 2. Verificar se já existe um membro com o nome "Adão".
        membro_adao = db.query(membros.Membro).filter(membros.Membro.nomeCompleto == "Adão").first()
        if not membro_adao:
            # Criar o membro "Adão"
            membro_adao = membros.Membro(
                nomeCompleto="Adão",
                cpf="11111111111",  # CPF fictício
                dataNascimento="1990-01-01",  # Data de nascimento fictícia
                telefone="11-1111-1111",  # Telefone fictício
                rua="Rua Principal",
                numero="1",
                bairro="Centro",
                cidade="Cidade",
                naturalidade="Local",
                dataInclusao="2023-01-01"  # Data fictícia
            )
            db.add(membro_adao)
            db.commit()
            db.refresh(membro_adao)

        # 3. Verificar se o usuário "Adão" já existe.
        usuario_adao = db.query(usuarios.Usuario).filter(usuarios.Usuario.login == "adao").first()
        if not usuario_adao:
            # Criar o usuário "Adão"
            hashed_password = get_password_hash("123456")
            usuario_adao = usuarios.Usuario(login="adao", password=hashed_password, idMembro=membro_adao.idMembro)
            db.add(usuario_adao)
            db.commit()
            db.refresh(usuario_adao)

        # 4. Criar o registro na tabela 'meal' (se necessário).
        meal_adao = db.query(meal.Meal).filter(meal.Meal.idMembro == membro_adao.idMembro).first()
        if not meal_adao:
             meal_adao = meal.Meal(idMembro=membro_adao.idMembro, idCargo=cargo_senior.idCargo, dataPosse="2023-01-01")
             db.add(meal_adao)
             db.commit()
             db.refresh(meal_adao)

        print("Usuario Adão criado/verificado com sucesso!")

    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    init_db()
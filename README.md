# Igreja API

Uma API RESTful construída com FastAPI para gerenciar informações de membros, cargos, finanças e usuários de uma igreja.

## Pré-requisitos

- Python 3.8+
- MySQL Server

## Configuração Inicial

### 1. Criar o Ambiente Virtual

Navegue até o diretório do projeto no terminal e crie um ambiente virtual:

```bash
python3 -m venv venv  # ou python -m venv venv
```

### 2. Ativar o Ambiente Virtual

- **No Windows:**

  ```bash
  .\venv\Scripts\activate
  ```

- **No Linux/macOS:**

  ```bash
  source venv/bin/activate
  ```

### 3. Criar o Banco de Dados MySQL

Faça login no seu servidor MySQL e crie um banco de dados chamado `ices` (ou outro nome de sua preferência):

```sql
CREATE DATABASE ices CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Substitua `ices` pelo nome que você escolher. Lembre-se de atualizar o arquivo `.env` com o mesmo nome.

### 4. Configurar o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo, adaptando as credenciais do banco de dados:

```
DATABASE_URL=mysql+pymysql://'seu usuário':'sua senha'@localhost/'banco de dados que foi criado'
SECRET_KEY="sua chave secreta"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- `DATABASE_URL`: A URL de conexão com o seu banco de dados MySQL.
- `SECRET_KEY`: Uma chave secreta para a geração de tokens JWT. **Altere isso para uma chave segura em produção!**
- `ALGORITHM`: O algoritmo usado para a geração de tokens JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: O tempo de expiração dos tokens JWT em minutos.

### 5. Instalar as Dependências

Instale as dependências do projeto usando o `pip`:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém a lista de dependências:

```
fastapi
uvicorn
python-decouple
sqlalchemy
mysql-connector-python
passlib
python-jose[cryptography]
alembic
pymysql
python-multipart
bcrypt
```

### 6. Configurar o Alembic

O Alembic é usado para gerenciar as migrações do banco de dados.

#### Arquivo `alembic.ini`:

```ini
[alembic]
script_location = alembic
prepend_sys_path = .

version_path_separator = os

sqlalchemy.url = mysql+pymysql://'seu usuário':'sua senha'@localhost/'banco de dados que foi criado'

[post_write_hooks]
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

#### Arquivo `alembic/env.py`:

```python
import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context
from decouple import config

sys.path.append(os.getcwd())

from app.models import membros, cargos, usuarios, meal, entradas, saidas

config_alembic = context.config

if config_alembic.config_file_name is not None:
    fileConfig(config_alembic.config_file_name)

from database import Base
target_metadata = Base.metadata

def get_url():
    return config("DATABASE_URL")

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 7. Executar as Migrações do Alembic

Para criar as tabelas no banco de dados, execute os seguintes comandos do Alembic:

```bash
alembic upgrade head
```

Se você precisar gerar uma nova migração após alterar os modelos:

```bash
alembic revision --autogenerate -m "Descrição da alteração"
alembic upgrade head
```

### 8. Executar a Aplicação

Execute a aplicação FastAPI com Uvicorn:

```bash
uvicorn main:app --reload
```

### 9. Acessar a Documentação da API

Acesse a documentação interativa da API (Swagger UI) em:

```
http://127.0.0.1:8000/docs#/
```

## Estrutura do Projeto

```
igreja_api/
├── main.py
├── database.py
├── init_db.py
├── alembic.ini
├── .env
├── requirements.txt
├── .gitignore
├── alembic/
│   ├── env.py
│   ├── versions/
│   │   └── <versao_inicial>.py
│   └── script.py.mako
└── app/
    ├── core/
    │   ├── security.py
    │   └── settings.py
    ├── routes/
    │   ├── auth.py
    │   ├── membros.py
    │   ├── cargos.py
    │   ├── usuarios.py
    │   ├── meal.py
    │   ├── entradas.py
    │   └── saidas.py
    ├── crud/
    │   ├── membros.py
    │   ├── cargos.py
    │   ├── usuarios.py
    │   ├── meal.py
    │   ├── entradas.py
    │   └── saidas.py
    ├── schemas/
    │   ├── membros.py
    │   ├── cargos.py
    │   ├── usuarios.py
    │   ├── meal.py
    │   ├── entradas.py
    │   └── saidas.py
    ├── models/
    │   ├── membros.py
    │   ├── cargos.py
    │   ├── usuarios.py
    │   ├── meal.py
    │   ├── entradas.py
    │   └── saidas.py
```

Este guia fornece o básico para configurar e executar a sua API. Adapte-o de acordo com as suas necessidades específicas e adicione mais informações conforme necessário.

```

**Observações:**

*   **Segurança:**  Reforce a importância de usar uma `SECRET_KEY` segura em produção.
*   **Credenciais:** Deixe claro que as credenciais do banco de dados no `.env` devem ser mantidas em segredo e nunca commitadas no Git.
*   **Adaptação:** Incentive os usuários a adaptar a documentação às suas necessidades.
```

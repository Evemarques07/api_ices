from fastapi import FastAPI
from app.routes import membros, cargos, usuarios, meal, entradas, saidas, auth, avisos
from database import engine
from app.models import membros as membros_model
from app.models import cargos as cargos_model
from app.models import usuarios as usuarios_model
from app.models import meal as meal_model
from app.models import entradas as entradas_model
from app.models import saidas as saidas_model
from app.models import avisos as avisos_model
from init_db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    membros_model.Base.metadata.create_all(bind=engine)
    cargos_model.Base.metadata.create_all(bind=engine)
    usuarios_model.Base.metadata.create_all(bind=engine)
    meal_model.Base.metadata.create_all(bind=engine)
    entradas_model.Base.metadata.create_all(bind=engine)
    saidas_model.Base.metadata.create_all(bind=engine)
    avisos_model.Base.metadata.create_all(bind=engine)
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(membros.router, prefix="/membros", tags=["membros"])
app.include_router(cargos.router, prefix="/cargos", tags=["cargos"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(meal.router, prefix="/meal", tags=["meal"])
app.include_router(entradas.router, prefix="/entradas", tags=["entradas"])
app.include_router(saidas.router, prefix="/saidas", tags=["saidas"])
app.include_router(avisos.router, prefix="/avisos", tags=["avisos"])
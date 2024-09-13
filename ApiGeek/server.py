from fastapi import FastAPI
from controllers_geek import router
from database import sync_database, get_engine

""" criando um objeto de FastaApi """
app = FastAPI()

""" inicializar o banco de dados """
sync_database(get_engine())

""" compilando a rota """
app.include_router(router, prefix="/api")
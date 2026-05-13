from core import settings, db_manager
from routes import proveedor_router
from contextlib import asynccontextmanager
from fastapi import FastAPI

#ESTO ES EL CICLO DE VIDA DE LA APLICACIÓN PERO EN ASYNC PARA Q JALE MÁS CHIDO
#XD EL ASYNC ES PARA Q PUEDA MANEJAR MEJOR LAS CONEXIONES
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicio")
    db_manager.connect()
    yield
    db_manager.close_all()
    print("fin")

app = FastAPI(lifespan=lifespan)

app.include_router(proveedor_router)

@app.get("/")
def root():
    return {"message": "Hola Mundo", "status": "ok"}
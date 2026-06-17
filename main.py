from core import settings, db_manager
from routes import *
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(calendario_router)
app.include_router(cava_router)
app.include_router(general_router)
app.include_router(busqueda_router)
app.include_router(vino_stats_router)

@app.get("/")
def root():
    return {"message": "Hola Mundo", "status": "ok"}
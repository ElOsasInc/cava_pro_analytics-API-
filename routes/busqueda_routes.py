from fastapi import APIRouter, Depends
from core import get_db
from controllers import BusquedaController
from models import Busqueda

router = APIRouter(prefix="/buscar", tags=["buscar"])

def get_controller(db = Depends(get_db)):
    return BusquedaController(db)

@router.get("/")
def filtrar_busqueda(busqueda: Busqueda, controller: BusquedaController = Depends(get_controller)):
    return controller.buscar(busqueda)
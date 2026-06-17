from fastapi import APIRouter, Depends, Query
from core import get_db
from controllers import VinoStatsController
from models import Busqueda1Vino
from typing import Optional
from datetime import date

router = APIRouter(prefix="/vino_stats", tags=["Vino stats"])

def get_controller(db = Depends(get_db)):
    return VinoStatsController(db)

@router.get("/")
def get_vino_stats(vino_key: int = Query(...), ini: Optional[date] = Query(None), fin: Optional[date] = Query(None), controller: VinoStatsController = Depends(get_controller)):
    rango = Busqueda1Vino(vino_key=vino_key)
    if(ini != None):
        rango.fecha_inicio = ini
    if(fin != None):
        rango.fecha_fin = fin
    return controller.get_vino_stats(rango)
from fastapi import APIRouter, Depends, Query
from core import get_db
from controllers import BusquedaController
from models import Busqueda, Parametro
from typing import List, Optional
from itertools import zip_longest
from datetime import date

router = APIRouter(prefix="/buscar", tags=["buscar"])

def get_controller(db = Depends(get_db)):
    return BusquedaController(db)

@router.get("/")
def filtrar_busqueda(c: Optional[List[str]] = Query([]), v: Optional[List[str]] = Query([]), ini: Optional[date] = Query(None), fin: Optional[date] = Query(None), controller: BusquedaController = Depends(get_controller)):
    parametros = []
    for clase, valor in zip_longest(c, v, fillvalue=None):
        parametros.append(Parametro(clase=clase, parametro=valor))
    busqueda = Busqueda(parametros=parametros, fecha_inicio=ini, fecha_fin=fin)
    return controller.buscar(busqueda, c)
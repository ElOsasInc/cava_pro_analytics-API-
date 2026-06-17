from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, timedelta

class Parametro(BaseModel):
    clase: str
    parametro: Optional[str]

class Busqueda(BaseModel):
    parametros: Optional[List[Parametro]]
    fecha_inicio: Optional[date] = date.today()
    fecha_fin: Optional[date] = (date.today() - timedelta(days=30))
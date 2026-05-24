from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Parametro(BaseModel):
    clase: str
    parametro: str

class Busqueda(BaseModel):
    parametros: Optional[List[Parametro]]
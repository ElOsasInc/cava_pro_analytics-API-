from models import PosicionBotellaModel
from typing import Dict, List, Any
from fastapi import HTTPException, status

class CavaController:
    def __init__(self, db_connection):
        self.model = PosicionBotellaModel(db_connection)

    def get_full_cava(self) -> List[Dict[str, Any]]:
        try:
            cava = self.model.get_filas()
            for fila in cava:
                fila["botellas"] = self.model.get_detalle_fila(fila["fila"])
            return cava
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema al obtener la cava: {str(e)}"
            )
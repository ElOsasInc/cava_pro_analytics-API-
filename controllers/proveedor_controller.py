from typing import List, Dict, Any
from fastapi import HTTPException, status
from models import ProveedorModel

class ProveedorController:
    def __init__(self, db_connection):
        self.model = ProveedorModel(db_connection)

    def get_all_proveedores(self) -> List[Dict[str, Any]]:
        try:
            return self.model.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener todos los proveedores: {str(e)}"
            )
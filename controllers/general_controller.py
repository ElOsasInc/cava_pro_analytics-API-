from models import ProveedorModel, VinoModel
from typing import List, Dict, Any
from fastapi import HTTPException, status

class GeneralController:
    def __init__(self, db_connection):
        self.proveedor_model = ProveedorModel(db_connection)
        self.vino_model = VinoModel(db_connection)

    def get_selects(self) -> List[Dict[str, Any]]:
        try:
            selects = {}
            selects["proveedores"] = self.proveedor_model.lista_proveedores()
            selects["vinos"] = self.vino_model.lista_vinos()
            return selects
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema al obtener los selects: {str(e)}"
            )
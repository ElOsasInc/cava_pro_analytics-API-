from models import CalendarioModel
from typing import Dict, List, Any
from collections import defaultdict
from fastapi import HTTPException, status

class CalendarioController:
    def __init__(self, db_connection):
        self.calendario_model = CalendarioModel(db_connection)

    def get_full_calendario(self) -> List[Dict[str, Any]]:
        try:
            calendario = self.calendario_model.get_all_pedidos()
            return calendario
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema al obtener el calendario: {str(e)}"
            )
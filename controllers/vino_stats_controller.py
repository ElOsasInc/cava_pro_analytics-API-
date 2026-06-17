from models import VinoStatsModel, Busqueda1Vino
from typing import List, Dict, Any
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse

class VinoStatsController:
    def __init__(self, db_connection):
        self.vino_stats_model = VinoStatsModel(db_connection)
    
    def get_vino_stats(self, rango: Busqueda1Vino) -> List[Dict[str, Any]]:
        try:
            vino_stats = {
                "ventas_x_dia": {
                    "tipo": "Bar",
                    "data": self.vino_stats_model.ventas_x_dia(rango)
                },
                "ventas_x_dia_semana": {
                    "tipo": "Bar",
                    "data": self.vino_stats_model.ventas_x_dia_semana(rango)
                },
                "copa_x_botella": {
                    "tipo": "Bar",
                    "data": self.vino_stats_model.copa_x_botella(rango)
                },
                "historial_precios": {
                    "tipo": "Line",
                    "data": self.vino_stats_model.historial_precios(rango)
                }
            }
            return vino_stats
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema al buscar: {str(e)}"
            )
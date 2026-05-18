from models import DashboardModel
from typing import Dict, List, Any
from fastapi import HTTPException, status

class DashboardController:
    def __init__(self, db_connection):
        self.model = DashboardModel(db_connection)

    def get_dashboard_stats(self) -> List[Dict[str, Any]]:
        try:
            dashboard = {
                "ventas_30dias":{
                    "tipo":"Line",
                    "data": self.model.get_ventas_30dias()
                },
                "afluencia":{
                    "tipo": "Bar",
                    "data": self.model.get_afluencia()
                },
                "top5_prods_pedidos":{
                    "tipo": "Bar",
                    "data": self.model.get_top5_prods_pedidos()
                },
                "top5_vinos_vendidos":{
                    "tipo": "Bar",
                    "data": self.model.get_top5_vinos_vendidos()
                },
                "pedidos_10semanas":{
                    "tipo": "Line",
                    "data": self.model.get_pedidos_10semanas()
                },
                "costo_ganancia":{
                    "tipo": "Line",
                    "data": self.model.get_costo_ganancia()
                }
            }
            return dashboard
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema con las stats: {str(e)}"
            )

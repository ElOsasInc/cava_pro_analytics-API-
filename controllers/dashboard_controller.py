from models import DashboardModel
from typing import Dict, List, Any
from fastapi import HTTPException, status

class DashboardController:
    def __init__(self, db_connection):
        self.model = DashboardModel(db_connection)

    def get_dashboard_stats(self) -> List[Dict[str, Any]]:
        try:
            dashboard = {
                "ventas_30dias": self.model.get_ventas_30dias(),
                "afluencia": self.model.get_afluencia(),
                "top5_prods_pedidos": self.model.get_top5_prods_pedidos(),
                "top5_vinos_vendidos": self.model.get_top5_vinos_vendidos(),
                "pedidos_10semanas": self.model.get_pedidos_10semanas(),
                "costo_ganancia": self.model.get_costo_ganancia()
            }
            return dashboard
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema con las stats: {str(e)}"
            )

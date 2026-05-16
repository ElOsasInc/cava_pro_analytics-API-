from models import DashboardModel
from typing import Dict, List, Any
from fastapi import HTTPException, status

class DashboardController:
    def __init__(self, db_connection):
        self.model = DashboardModel(db_connection)

    def get_dashboard_stats(self) -> List[Dict[str, Any]]:
        try:
            dashboard = {
                "ventas_30dias": self.model.get_ventas_30dias()
            }
            return dashboard
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema con las stats: {str(e)}"
            )

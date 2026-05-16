from fastapi import APIRouter, Depends
from core import get_db
from controllers import DashboardController

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def get_controller(db = Depends(get_db)):
    return DashboardController(db)

@router.get("/")
def get_clientes(controller: DashboardController = Depends(get_controller)):
    return controller.get_dashboard_stats()
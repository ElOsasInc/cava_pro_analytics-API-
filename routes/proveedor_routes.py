from fastapi import APIRouter, Depends
from core import get_db
from controllers import ProveedorController

router = APIRouter(prefix="/proveedores", tags=["proveedores"])

def get_controller(db = Depends(get_db)):
    return ProveedorController(db)

@router.get("/")
def get_clientes(controller: ProveedorController = Depends(get_controller)):
    return controller.get_all_proveedores()
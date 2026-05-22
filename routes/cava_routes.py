from fastapi import APIRouter, Depends
from core import get_db
from controllers import CavaController

router = APIRouter(prefix="/cava", tags=["cava"])

def get_controller(db = Depends(get_db)):
    return CavaController(db)

@router.get("/")
def get_cava(controller: CavaController = Depends(get_controller)):
    return controller.get_full_cava()

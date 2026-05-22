from fastapi import APIRouter, Depends
from core import get_db
from controllers import CalendarioController

router = APIRouter(prefix="/calendario", tags=["calendario"])

def get_controller(db = Depends(get_db)):
    return CalendarioController(db)

@router.get("/")
def get_calendario(controller: CalendarioController = Depends(get_controller)):
    return controller.get_full_calendario()
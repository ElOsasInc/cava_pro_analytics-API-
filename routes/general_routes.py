from fastapi import APIRouter, Depends
from core import get_db
from controllers import GeneralController

router = APIRouter(prefix="/general", tags=["general"])

def get_controller(db = Depends(get_db)):
    return GeneralController(db)

@router.get("/")
def get_selects(controller: GeneralController = Depends(get_controller)):
    return controller.get_selects()
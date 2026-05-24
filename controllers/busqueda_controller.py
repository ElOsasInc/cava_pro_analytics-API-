from models import Busqueda
from typing import List, Dict, Any
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse

class BusquedaController:
    def __init__(self, db_connection):
        pass
        
    def buscar(self, busqueda: Busqueda) -> List[Dict[str, Any]]:
        try:
            parametros = busqueda.parametros
            match len(parametros):
                case 0:
                    return RedirectResponse(url="/dashboard/", status_code=303)
                case 1:
                    match parametros[0].clase:
                        case "vino":
                            return "vino"
                        case "proveedor":
                            return "proveedor"
                        case _:
                            raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"La búsqueda no existe"
                            )
                case 2:
                    pass
                case 3:
                    pass
                case _:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"La búsqueda no existe"
                    )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema al buscar: {str(e)}"
            )
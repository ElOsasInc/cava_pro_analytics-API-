from models import Busqueda
from typing import List, Dict, Any
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse

class BusquedaController:
    def __init__(self, db_connection):
        pass
    
    def buscar(self, busqueda: Busqueda, clases: List[str]) -> List[Dict[str, Any]]:
        try:
            parametros = busqueda.parametros
            no_clases = {"vinos": 0, "proveedores": 0}
            for clase in clases:
                if(clase == "vino"):
                    no_clases["vinos"] += 1
                elif(clase == "proveedor"):
                    no_clases["proveedores"] += 1
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"La clase {clase} no existe"
                    )
            match (no_clases["proveedores"] + no_clases["vinos"]):
                case 0:
                    return RedirectResponse(url="/dashboard/", status_code=303)
                case 1:
                    if(parametros[0].clase == "vino"):
                        return "stats vino"
                    elif(parametros[0].clase == "proveedor"):
                        return "stats proveedor"
                case 2:
                    if(no_clases["vinos"] == 2):
                        return "comparacion de vinos"
                    elif(no_clases["proveedores"] == 2):
                        return "comparacion de proveedores"
                    elif(no_clases["vinos"] == no_clases["proveedores"]):
                        return "stats vino en el proveedor"
                case 3:
                    #if()
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
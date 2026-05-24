from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Proveedor(BaseModel):
    proveedor_id: Optional[str] = None
    nombre: str
    telefono: int
    correo: str
    especialidad: Optional[str]
    tiempo_promedio: Optional[str]
    anotacion: Optional[str]

class ProveedorModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM proveedor")
            return cur.fetchall()
        
    def lista_proveedores(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT proveedor_id, nombre FROM proveedor
                ORDER BY nombre;
            """)
            return cur.fetchall()
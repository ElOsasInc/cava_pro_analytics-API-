from pydantic import BaseModel
from typing import Dict, List, Any

class PosicionBotellaModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_filas(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT(fila) FROM posicion_botella
                ORDER BY fila;
            """)
            return cur.fetchall()
        
    def get_detalle_fila(self, fila: str) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                SELECT 	columna, fila, b.id_botella, estado, ml_restantes,
                        v.vino_id, nombre, marca, lote,
                        tipo, region, cosecha, anejado, alcohol, volumen, descripcion, precio_botella, precio_copa
                FROM posicion_botella as pb
                INNER JOIN botella as b ON b.id_botella = pb.id_botella
                INNER JOIN vino as v ON v.vino_id = b.vino_id
                WHERE fila = '{fila}'
                ORDER BY columna, fila;
            """)
            return cur.fetchall()
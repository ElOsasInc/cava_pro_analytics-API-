from pydantic import BaseModel
from typing import Dict, List, Any

class PosicionBotellaModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all_posiciones(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT 	columna, fila, b.id_botella, estado, ml_restantes,
                        v.vino_id, nombre, marca, lote,
                        tipo, region, cosecha, anejado, alcohol, volumen, descripcion, precio_botella, precio_copa
                FROM posicion_botella as pb
                INNER JOIN botella as b ON b.id_botella = pb.id_botella
                INNER JOIN vino as v ON v.vino_id = b.vino_id
                ORDER BY columna, fila;
            """)
            return cur.fetchall()
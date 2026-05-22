from pydantic import BaseModel
from typing import List, Dict, Any

class ProductoPedidoModel():
    def __init__(self, db_connection):
        self.db = db_connection

    def get_detalle_pedido(self, pedido_id: str) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                SELECT lote, vino_id, cantidad, costo_unitario, (cantidad * costo_unitario) as subtotal
                FROM producto_pedido
                WHERE pedido_id = '{pedido_id}'
            """)
            return cur.fetchall()
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import date

class PedidoModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all_fechas_pedidos(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT(fecha_entrega) FROM pedido
                ORDER BY fecha_entrega;
            """)
            return cur.fetchall()
        
    def get_pedidos_fecha(self, fecha_entrega: date) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                SELECT pedido_id, pro.proveedor_id, pro.nombre as proveedor_nombre, fecha_pedido
                FROM pedido as p INNER JOIN proveedor as pro ON pro.proveedor_id = p.proveedor_id 
                WHERE fecha_entrega = '{fecha_entrega}'
                ORDER BY fecha_pedido;
            """)
            return cur.fetchall()
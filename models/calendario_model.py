from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import date

class CalendarioModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all_pedidos(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                WITH resumen_productos AS (
                    SELECT  hc.fecha_entrega_key,
                            hc.pedido_id_original, dp.proveedor_id_original, dp.nombre as proveedor_nombre, hc.fecha_key,
                            db.lote, dv.vino_id_original, dv.nombre as vino_nombre,
                            hc.precio_unitario, COUNT(dv.vino_id_original) as cantidad, (COUNT(dv.vino_id_original) * hc.precio_unitario) as subtotal
                    FROM hechos_compras hc
                    INNER JOIN dim_proveedor dp ON dp.proveedor_key = hc.proveedor_key
                    INNER JOIN dim_botella db ON db.botella_key = hc.botella_key
                    INNER JOIN dim_vino dv ON dv.vino_key = db.vino_key
                    GROUP BY    hc.fecha_entrega_key,
                                hc.pedido_id_original, dp.proveedor_id_original, dp.nombre, hc.fecha_key,
                                db.lote, dv.vino_id_original, dv.nombre,
                                hc.precio_unitario
                ),
                agrupado_pedidos AS (
                    SELECT 
                        fecha_entrega_key,
                        pedido_id_original,
                        proveedor_id_original,
                        proveedor_nombre,
                        fecha_key,
                        json_agg(
                            json_build_object(
                                'lote', lote,
                                'vino_id', vino_id_original,
                                'vino_nombre', vino_nombre,
                                'cantidad', cantidad,
                                'costo_unitario', precio_unitario,
                                'subtotal', subtotal
                            )
                            ORDER BY vino_nombre DESC
                        ) as productos
                    FROM resumen_productos
                    GROUP BY 
                        fecha_entrega_key,
                        pedido_id_original,
                        proveedor_id_original,
                        proveedor_nombre,
                        fecha_key
                )
                SELECT 
                    fecha_entrega_key as fecha_entrega,
                    json_agg(
                        json_build_object(
                            'pedido_id', pedido_id_original,
                            'proveedor_id', proveedor_id_original,
                            'proveedor_nombre', proveedor_nombre,
                            'fecha_pedido', fecha_key,
                            'productos', productos
                        )
                        ORDER BY fecha_key DESC
                    ) as pedidos
                FROM agrupado_pedidos
                GROUP BY fecha_entrega_key
                ORDER BY fecha_entrega DESC;
            """)
            return cur.fetchall()
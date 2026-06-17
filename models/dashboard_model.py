from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date

class DashboardModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_ventas_30dias(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT df.fecha_key as fecha, ROUND(COALESCE(SUM(hv.precio), 0)::NUMERIC, 2) as total_ventas
                FROM dim_fecha as df
                LEFT JOIN hechos_ventas as hv ON hv.fecha_key = df.fecha_key
                WHERE df.fecha_key BETWEEN (NOW() - INTERVAL '29 days')::DATE AND NOW()::DATE
                GROUP BY df.fecha_key
                ORDER BY df.fecha_key;
            """)
            return cur.fetchall()
        
    def get_afluencia(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                WITH horas as (
                    SELECT GENERATE_SERIES(0, 23, 1)::INT as hora
                )
                SELECT h.hora, COUNT(venta_key) as cant_ventas
                FROM hechos_ventas as hv
                RIGHT JOIN horas as h ON h.hora = EXTRACT('hour' FROM hv.hora)
                GROUP BY h.hora
                ORDER BY h.hora;
            """)
            return cur.fetchall()
        
    def get_top5_prods_pedidos(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT dv.nombre, COUNT(db.vino_key) as cantidad, ROUND(SUM(hc.precio_unitario)::NUMERIC, 2) as dinero_total
                FROM hechos_compras as hc
                INNER JOIN dim_botella as db ON db.botella_key = hc.botella_key
                INNER JOIN dim_vino as dv ON dv.vino_key = db.vino_key
                GROUP BY dv.nombre
                ORDER BY dv.nombre
                LIMIT 5;
            """)
            return cur.fetchall()
        
    def get_top5_vinos_vendidos(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT dv.nombre, SUM(ml) as ml_total, ROUND(SUM(precio)::NUMERIC, 2) as precio_total
                FROM hechos_ventas hv
                INNER JOIN dim_botella as db ON db.botella_key = hv.botella_key
                INNER JOIN dim_vino as dv ON dv.vino_key = db.vino_key
                GROUP BY dv.nombre
                ORDER BY ml_total DESC
                LIMIT 5;
            """)
            return cur.fetchall()
        
    def get_pedidos_10semanas(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT(DATE_TRUNC('week', fecha_key)::DATE) as semana, COALESCE(total_pedidos, 0) as total_pedidos
                FROM dim_fecha as df
                LEFT JOIN (
                    SELECT DATE_TRUNC('week', fecha_key)::DATE as semana, COUNT(DISTINCT(pedido_id_original)) as total_pedidos
                    FROM hechos_compras
                    GROUP BY semana
                    ORDER BY semana DESC
                ) as dp ON dp.semana = DATE_TRUNC('week', fecha_key)::DATE
                WHERE fecha_key <= NOW()::DATE
                GROUP BY df.fecha_key, df.semana, total_pedidos
                ORDER BY semana DESC
                LIMIT 10;
            """)
            return cur.fetchall()

    def get_costo_ganancia(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT CONCAT(anio,' ',mes_nombre) as mes, ROUND(SUM(precio)::NUMERIC, 2) as ganancia_total, ROUND(SUM(precio_unitario)::NUMERIC, 2) as costo_total
                FROM dim_fecha as df
                LEFT JOIN hechos_ventas as hv ON hv.fecha_key = df.fecha_key
                LEFT JOIN hechos_compras as hc ON hc.fecha_key = df.fecha_key
                WHERE df.fecha_key BETWEEN (NOW()::DATE - INTERVAL '11 months') AND NOW()::DATE
                GROUP BY CONCAT(anio,' ',mes_nombre)
                ORDER BY TO_DATE(CONCAT(anio,' ',mes_nombre), 'YYYY MON');
            """)
            return cur.fetchall()
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date

class VentaDia(BaseModel):
    fecha: date
    total_ventas: float

class AlfuenciaHora(BaseModel):
    hora: int
    cant_ventas: int

class ProductoPedidoTop(BaseModel):
    nombre: str
    cantidad: int
    costo_total: float

class VinoVendidoTop(BaseModel):
    nombre: str
    ml_total: int
    precio_total: float

class PedidoSemana(BaseModel):
    semana: date
    total_pedidos: int

class CostoGananciaMes(BaseModel):
    mes: str
    costo_total: float
    ganancia_total: float

class Dashboard(BaseModel):
    ventas_30dias: List[VentaDia] = []
    afluencia: List[AlfuenciaHora] = []
    top5_prods_pedidos: List[ProductoPedidoTop] = []
    top5_vinos_vendidos: List[VinoVendidoTop] = []
    pedidos_10semanas: List[PedidoSemana] = []
    costo_ganancia: List[CostoGananciaMes] = []

class DashboardModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_ventas_30dias(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                WITH fechas as (
                    SELECT GENERATE_SERIES(
                        (NOW() - INTERVAL '29 days')::DATE, NOW()::DATE, '1 day'::INTERVAL
                    )::DATE as fecha
                )
                SELECT f.fecha, COALESCE(SUM(pv.registro_precio), 0) as total_ventas
                FROM fechas as f
                LEFT JOIN venta v ON v.fecha_hora::DATE = f.fecha
                LEFT JOIN producto_vendido as pv ON pv.id_venta = v.id_venta
                GROUP BY f.fecha
                ORDER BY f.fecha;
            """)
            return cur.fetchall()
        
    def get_afluencia(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                WITH horas as (
                    SELECT GENERATE_SERIES(0, 23, 1)::INT as hora
                )
                SELECT h.hora, COALESCE(cant_ventas, 0) as cant_ventas
                FROM horas as h
                LEFT JOIN (
                    SELECT EXTRACT(HOUR FROM fecha_hora) as hora, COUNT(id_venta) as cant_ventas
                    FROM venta
                    GROUP BY hora
                ) as v ON h.hora = v.hora
                ORDER BY h.hora;
            """)
            return cur.fetchall()
        
    def get_top5_prods_pedidos(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT v.nombre, SUM(cantidad) as cantidad, ROUND(SUM(costo_unitario*cantidad)::NUMERIC, 2) as dinero_total
                FROM producto_pedido as pp INNER JOIN vino as v ON v.vino_id = pp.vino_id
                GROUP BY v.nombre
                ORDER BY cantidad DESC
                LIMIT 5;
            """)
            return cur.fetchall()
        
    def get_top5_vinos_vendidos(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT nombre, SUM(ml) as ml_total, ROUND(SUM(registro_precio)::NUMERIC, 2) as precio_total
                FROM producto_vendido as pv
                INNER JOIN botella as b ON b.id_botella = pv.id_botella INNER JOIN vino as v ON v.vino_id = b.vino_id
                GROUP BY nombre
                ORDER BY ml_total DESC
                LIMIT 5;
            """)
            return cur.fetchall()
        
    def get_pedidos_10semanas(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                WITH semanas as (
                    SELECT GENERATE_SERIES(
                        DATE_TRUNC('week', (NOW() - INTERVAL '9 weeks'))::DATE,
                        DATE_TRUNC('week', NOW())::DATE, '1 week'::INTERVAL
                    )::DATE as semana
                )
                SELECT s.semana, COALESCE(total_pedidos, 0) as total_pedidos
                FROM semanas as s
                INNER JOIN (
                    SELECT DATE_TRUNC('week', fecha_pedido)::DATE as semana, COUNT(pedido_id) as total_pedidos
                    FROM pedido
                    GROUP BY semana
                ) as p ON p.semana = s.semana
                ORDER BY semana;
            """)
            return cur.fetchall()

    def get_costo_ganancia(self) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute("""
                WITH meses as (
                    SELECT TO_CHAR(GENERATE_SERIES( 
                        (NOW() - INTERVAL '11 months')::DATE, NOW()::DATE, '1 month'::INTERVAL
                    )::DATE, 'YYYY MON') as mes
                )
                SELECT m.mes, COALESCE(costo_total, 0.00) as costo_total, COALESCE(ganancia_total, 0.00) as ganancia_total
                FROM meses as m
                INNER JOIN (
                    SELECT TO_CHAR(fecha_pedido, 'YYYY MON') as mes, ROUND(SUM(costo_unitario*cantidad)::NUMERIC, 2) as costo_total, g.ganancia_total
                    FROM producto_pedido as pp INNER JOIN pedido as p ON p.pedido_id = pp.pedido_id
                    FULL OUTER JOIN (
                        SELECT TO_CHAR(fecha_hora, 'YYYY MON') as mes, ROUND(SUM(registro_precio)::NUMERIC, 2) as ganancia_total
                        FROM producto_vendido as pv INNER JOIN venta as v ON v.id_venta = pv.id_venta
                        GROUP BY mes
                    ) as g ON g.mes = TO_CHAR(fecha_pedido, 'YYYY MON')
                    GROUP BY TO_CHAR(fecha_pedido, 'YYYY MON'), g.ganancia_total
                ) as cg ON cg.mes = m.mes
                ORDER BY TO_DATE(m.mes, 'YYYY MON');
            """)
            return cur.fetchall()
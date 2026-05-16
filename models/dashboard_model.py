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
        
    

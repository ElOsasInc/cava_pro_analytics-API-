from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date, timedelta

class Busqueda1Vino(BaseModel):
    vino_key: int
    fecha_inicio: Optional[date] = (date.today() - timedelta(days=30))
    fecha_fin: Optional[date] = date.today()

class VinoStatsModel:
    def __init__(self, db_connection):
        self.db = db_connection

    def ventas_x_dia(self, rango: Busqueda1Vino) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f'''
                SELECT df.fecha_key as fecha, ROUND(COALESCE(ganancia_dia, 0)::NUMERIC, 2) as ganancia_dia, COALESCE(cantidad_dia, 0) as cantidad_dia
                FROM dim_fecha as df
                LEFT JOIN (
                    SELECT hv.fecha_key, SUM(precio) as ganancia_dia, COUNT(venta_key) as cantidad_dia
                    FROM hechos_ventas as hv
                    INNER JOIN dim_botella as db ON db.botella_key = hv.botella_key
                    INNER JOIN dim_vino as dv ON dv.vino_key = db.vino_key
                    WHERE db.vino_key = {rango.vino_key}
                    GROUP BY hv.fecha_key
                ) as rv ON rv.fecha_key = df.fecha_key
                WHERE df.fecha_key BETWEEN '{rango.fecha_inicio}' AND '{rango.fecha_fin}'
                ORDER BY df.fecha_key;
            ''')
            return cur.fetchall()
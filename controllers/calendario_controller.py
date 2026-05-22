from models import PedidoModel, ProductoPedidoModel
from typing import Dict, List, Any
from fastapi import HTTPException, status

class CalendarioController:
    def __init__(self, db_connection):
        self.pedido_model = PedidoModel(db_connection)
        self.producto_pedido_model = ProductoPedidoModel(db_connection)

    def get_full_calendario(self) -> List[Dict[str, Any]]:
        try:
            calendario = self.pedido_model.get_all_fechas_pedidos()
            for fecha in calendario:
                fecha["pedidos"] = self.pedido_model.get_pedidos_fecha(fecha['fecha_entrega'])
                for pedido in fecha["pedidos"]:
                    pedido["total"] = 0
                    pedido["prodcutos"] = self.producto_pedido_model.get_detalle_pedido(pedido["pedido_id"])
                    for producto in pedido["prodcutos"]:
                        pedido["total"] += producto["subtotal"]
            return calendario
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Problema al obtener el calendario: {str(e)}"
            )
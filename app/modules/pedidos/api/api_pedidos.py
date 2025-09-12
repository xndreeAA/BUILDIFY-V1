from flask import Blueprint
from app.modules.pedidos.controller.pedido_controller import PedidoController

pedidos_bp = Blueprint('api_pedidos', __name__, url_prefix='/pedidos')

pedidos_bp.add_url_rule("/", view_func=PedidoController.obtener_pedidos, methods=['GET'])
pedidos_bp.add_url_rule("/categoria", view_func=PedidoController.obtener_pedidos_categoria, methods=['GET'])
pedidos_bp.add_url_rule("/usuario/<int:id_usuario>", view_func=PedidoController.obtener_pedidos_usuario, methods=['GET'])
pedidos_bp.add_url_rule("/historial-ventas-totales", view_func=PedidoController.obtener_historial_ventas_totales, methods=['GET'])
pedidos_bp.add_url_rule("/mas-menos", view_func=PedidoController.obtener_pedidos_mas_menos, methods=['GET'])
pedidos_bp.add_url_rule("/get-pedido-by-session", view_func=PedidoController.get_pedido_by_session, methods=['GET'])


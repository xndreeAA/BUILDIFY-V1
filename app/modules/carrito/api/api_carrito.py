from flask import Blueprint
from app.modules.carrito.controller.carrito_controller import CarritoController

carrito_bp = Blueprint('api_carrito', __name__, url_prefix='/carrito')

carrito_bp.add_url_rule("/", view_func=CarritoController.obtener_carrito, methods=["GET"])
carrito_bp.add_url_rule("/", view_func=CarritoController.anadir_producto_carrito, methods=["POST"])
carrito_bp.add_url_rule("/", view_func=CarritoController.eliminar_producto_carrito, methods=["DELETE"])
carrito_bp.add_url_rule("/", view_func=CarritoController.modificar_cantidad_producto_carrito, methods=["PUT"])
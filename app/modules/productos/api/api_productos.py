from flask import Blueprint
from app.modules.productos.controller.producto_controller import ProductoController

productos_bp = Blueprint('api_productos', __name__, url_prefix='/productos')

productos_bp.add_url_rule("/", view_func=ProductoController.obtener_productos, methods=["GET"])
productos_bp.add_url_rule("/", view_func=ProductoController.crear_producto, methods=["POST"])
productos_bp.add_url_rule("/<int:id_producto>", view_func=ProductoController.traer_un_producto, methods=["GET"])
productos_bp.add_url_rule("/<int:id_producto>", view_func=ProductoController.modificar_producto, methods=["PUT"])
productos_bp.add_url_rule("/<int:id_producto>", view_func=ProductoController.eliminar_producto, methods=["DELETE"])
productos_bp.add_url_rule("/subir-imagen", view_func=ProductoController.subir_imagenes_producto, methods=["POST"])

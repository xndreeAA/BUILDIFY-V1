from flask import Blueprint
from app.modules.usuarios.api.api_usuarios import usuarios_api_bp
from app.modules.carrito.api.api_carrito import carrito_bp

from app.modules.productos.api.api_productos import productos_bp
from app.modules.productos.api.api_marcas import marcas_bp
from app.modules.productos.api.api_categorias import categorias_bp
from app.modules.productos.api.api_detalles import detalles_bp

from app.modules.pedidos.api.api_pedidos import pedidos_bp
from app.modules.pagos.api.api_checkout import checkout_api_bp
from app.modules.pagos.api.api_webhook import webhook_api_bp

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api_v1.register_blueprint(usuarios_api_bp, url_prefix='/usuarios')
api_v1.register_blueprint(carrito_bp, url_prefix='/carrito')

api_v1.register_blueprint(productos_bp, url_prefix='/productos')
api_v1.register_blueprint(marcas_bp, url_prefix='/marcas')
api_v1.register_blueprint(categorias_bp, url_prefix='/categorias')
api_v1.register_blueprint(detalles_bp, url_prefix='/detalles')

api_v1.register_blueprint(pedidos_bp, url_prefix='/pedidos')
api_v1.register_blueprint(checkout_api_bp, url_prefix='/checkout')
api_v1.register_blueprint(webhook_api_bp, url_prefix='/checkout/webhook')

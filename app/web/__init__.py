from flask import Blueprint
from app.modules.auth.routes.auth_routes import auth_routes_bp
from app.modules.usuarios.routes.user_routes import usuario_routes_bp
from app.modules.usuarios.routes.admin_routes import admin_routes_bp
from app.modules.carrito.routes.carrito_routes import carrito_routes_bp
from app.modules.pagos.routes.pagos_routes import pagos_routes_bp

web_v1 = Blueprint('web_v1', __name__)

web_v1.register_blueprint(auth_routes_bp)
web_v1.register_blueprint(usuario_routes_bp)
web_v1.register_blueprint(admin_routes_bp, url_prefix='/admin', name_prefix='admin.')
web_v1.register_blueprint(carrito_routes_bp, url_prefix='/carrito', name_prefix='carrito.')
web_v1.register_blueprint(pagos_routes_bp, url_prefix='/pagos', name_prefix='pagos.')


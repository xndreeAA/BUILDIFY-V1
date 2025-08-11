from flask import Blueprint
from app.modules.auth.routes.auth_routes import auth_routes_bp
from app.modules.usuarios.routes.user_routes import usuario_routes_bp
from app.modules.usuarios.routes.admin_routes import admin_routes_bp

web_v1 = Blueprint('web_v1', __name__)

web_v1.register_blueprint(auth_routes_bp)
web_v1.register_blueprint(usuario_routes_bp)
web_v1.register_blueprint(admin_routes_bp)
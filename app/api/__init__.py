from flask import Blueprint
from app.modules.usuarios.api.api_usuarios import usuarios_api_bp

# Blueprint raíz para versionado
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Registro de APIs por módulo
api_v1.register_blueprint(usuarios_api_bp, url_prefix='/usuarios')
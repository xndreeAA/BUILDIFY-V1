from flask import Blueprint
from app.modules.auth.controllers import auth_controller
from app.modules.auth.controllers.auth_controller import (
    login, logout, register, forgot_password, reset_password
)

# Crea el blueprint
auth_routes_bp = Blueprint('auth', __name__)

# ------------------ RUTAS DE AUTENTICACIÓN ------------------ #
# Importa las funciones del controlador de autenticación
# Login
auth_routes_bp.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])

# Logout
auth_routes_bp.add_url_rule('/logout', view_func=logout)

# Registro
auth_routes_bp.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])

# ------------------ RUTAS DE RECUPERACIÓN DE CONTRASEÑA ------------------ #

# Olvidé mi contraseña
auth_routes_bp.add_url_rule('/forgot-password', view_func=forgot_password, methods=['GET', 'POST'])

# Restablecer contraseña con token
auth_routes_bp.add_url_rule('/reset-password/<token>', view_func=reset_password, methods=['GET', 'POST'])

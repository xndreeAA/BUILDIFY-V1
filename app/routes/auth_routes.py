from flask import Blueprint
from app.controllers import auth_controller
from app.controllers.auth_controller import login, logout, register


# Crea un blueprint 
auth_bp = Blueprint('auth', __name__)

# Ruta para iniciar sesión (soporta GET para mostrar el formulario y POST para procesar el login)
auth_bp.route('/login', methods=['GET', 'POST'])(auth_controller.login)

auth_bp.route('/logout')(auth_controller.logout)

auth_bp.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
auth_bp.add_url_rule('/logout', view_func=logout)
auth_bp.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])  # 👈 NUEVA RUTA
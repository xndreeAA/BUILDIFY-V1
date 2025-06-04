from flask import Blueprint
from app.controllers import auth_controller


# Crea un blueprint 
auth_bp = Blueprint('auth', __name__)

# Ruta para iniciar sesión (soporta GET para mostrar el formulario y POST para procesar el login)
auth_bp.route('/login', methods=['GET', 'POST'])(auth_controller.login)

auth_bp.route('/logout')(auth_controller.logout)

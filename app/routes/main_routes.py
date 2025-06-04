from flask import Blueprint, redirect, url_for

# Crea un blueprint principal para la raíz del sitio
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Redirige automáticamente a /login
    return redirect(url_for('auth.login'))

from flask import Blueprint
from flask import render_template

# Crea un blueprint principal para la raíz del sitio
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def home():
    return render_template('user/home.html')

@user_bp.route('/section')
def section():
    return render_template('user/section.html')

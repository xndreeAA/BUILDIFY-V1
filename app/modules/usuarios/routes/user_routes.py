from flask import Blueprint
from flask import render_template, Blueprint
from flask_login import login_required, current_user 
import requests
import os

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

usuario_routes_bp = Blueprint(
    'user',
    __name__,
    template_folder=template_dir,
    static_folder=static_dir,             
    static_url_path='/usuarios/static'    
)

@usuario_routes_bp.route('/')
def home():
    return render_template('user/home.html')

@usuario_routes_bp.route('/section/<category>')
def section(category):
    response = requests.get(f'http://127.0.0.1:5000/api/v1/productos?categoria={category}')
    
    if response.ok:
        products = response.json().get("data", [])
    else:
        products = []
    return render_template('user/section.html', products=products, category=category)
# ----------------------------------------------------------------
@usuario_routes_bp.route('/brand_view')
def brand_view():
    return render_template('user/brand_view.html')
# ----------------------------------------------------------------

@usuario_routes_bp.route('/product_details/<int:id>')
def product_details(id):
    return render_template('user/product_details.html', product_id=id)

@usuario_routes_bp.route('/mi_perfil')
@login_required
def mi_perfil():
    return render_template('user/user_perfil/' + 'user_perfil.html')

@usuario_routes_bp.route('/estado_pedidos')
@login_required
def estado_pedidos():
    return render_template('user/user_perfil/' + 'estado_pedidos.html')

@usuario_routes_bp.route('/configuracion_perfil')
@login_required
def configuracion_perfil():
    return render_template('user/user_perfil/' + 'configuracion_perfil.html')

# ------------------------------------------------------------------------
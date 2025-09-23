from flask import Blueprint, render_template
from flask_login import login_required, current_user 
import os
from app.modules.productos.services.producto_services import ProductoServices

# Rutas de templates y estáticos
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

usuario_routes_bp = Blueprint(
    'user',
    __name__,
    template_folder=template_dir,
    static_folder=static_dir,
    static_url_path='/usuarios/static'
)

# Base URL configurable (local y producción)
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

@usuario_routes_bp.route('/')
def home():
    return render_template('user/home.html')

@usuario_routes_bp.route('/section/<category>')
def section(category):
    try:
        # Llamada directa al servicio en lugar de requests.get
        data, status = ProductoServices.obtener_productos(
            busqueda=None,
            categoria_nombre=category.lower(),
            marca_nombre=None
        )
        products = data.get("data", []) if status == 200 else []
    except Exception as e:
        print(f"Error al obtener productos de {category}: {e}")
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
    return render_template('user/user_perfil/user_perfil.html')

@usuario_routes_bp.route('/estado_pedidos')
@login_required
def estado_pedidos():
    return render_template('user/user_perfil/estado_pedidos.html')

@usuario_routes_bp.route('/configuracion_perfil')
@login_required
def configuracion_perfil():
    return render_template('user/user_perfil/configuracion_perfil.html')
# ------------------------------------------------------------------------

from flask import Blueprint, render_template
from flask_login import login_required
import os

# ---------------------------------------------------------------------
# Configuración de carpetas para el Blueprint
# ---------------------------------------------------------------------
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

productos_routes_bp = Blueprint(
    'productos',
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)

# ---------------------------------------------------------------------
# Rutas de Productos
# ---------------------------------------------------------------------
@productos_routes_bp.route('/crud-productos')
@login_required
def crud_productos():
    return render_template('crud_productos/crud-productos.html')

@productos_routes_bp.route('/crear-productos')
@login_required
def crear_productos():
    return render_template('crud_productos/crear-productos.html')

# ---------------------------------------------------------------------
# Rutas de Marcas
# ---------------------------------------------------------------------
@productos_routes_bp.route('/crud-marcas')
@login_required
def crud_marcas():
    return render_template('crud_marcas/crud-marcas.html')

@productos_routes_bp.route('/crear-marcas')
@login_required
def crear_marcas():
    return render_template('crud_marcas/crear-marcas.html')

# ---------------------------------------------------------------------
# Rutas de Categorías
# ---------------------------------------------------------------------
@productos_routes_bp.route('/crud-categorias')
@login_required
def crud_categorias():
    return render_template('crud_categorias/crud-categorias.html')

@productos_routes_bp.route('/crear-categorias')
@login_required
def crear_categorias():
    return render_template('crud_categorias/crear-categorias.html')

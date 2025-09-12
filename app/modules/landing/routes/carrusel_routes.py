from flask import Blueprint, render_template
from flask_login import login_required
import os

# ---------------------------------------------------------------------
# Configuración de carpetas para el Blueprint
# ---------------------------------------------------------------------
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

carrusel_routes_bp = Blueprint(
    'carrusel',
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)
# ---------------------------------------------------------------------
# Ruta para la vista de CRUD de carrusel
# ---------------------------------------------------------------------
@carrusel_routes_bp.route('/crud-carrusel')
@login_required
def crud_carrusel():
    return render_template('crud_carrusel/crud-carrusel.html')
# ---------------------------------------------------------------------
# Ruta para la vista de creación de carrusel
# ---------------------------------------------------------------------
@carrusel_routes_bp.route('/crear-carrusel')
@login_required
def crear_carrusel():
    return render_template('crud_carrusel/crear-carrusel.html')

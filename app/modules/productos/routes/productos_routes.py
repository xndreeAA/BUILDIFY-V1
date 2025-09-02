from flask import Blueprint, jsonify, render_template, request, abort
from flask_login import login_required, current_user
import os
    
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

productos_routes_bp = Blueprint(
    'productos', 
    __name__, 
    template_folder=template_dir, 
    static_folder=static_dir
)

@productos_routes_bp.route('/crud-productos')
@login_required
def crud_productos():
    return render_template('crud-productos.html')

@productos_routes_bp.route('/crear-productos')
@login_required
def crear_productos():
    return render_template('crear-productos.html')

@productos_routes_bp.route('/crud-marcas.html')
@login_required
def crud_marcas():
    return render_template('crud-marcas.html')

@productos_routes_bp.route('/crear-marcas')
@login_required
def crear_marcas():
    return render_template('crear-marcas.html')

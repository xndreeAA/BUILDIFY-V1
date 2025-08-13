from flask import Blueprint, jsonify, render_template, request, abort
from flask_login import login_required, current_user
import os
    
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

produtos_routes_bp = Blueprint(
    'productos', 
    __name__, 
    template_folder=template_dir, 
    static_folder=static_dir
)


@produtos_routes_bp.route('/productos')
@login_required
def crud_productos():
    return render_template('crud-productos.html')

@produtos_routes_bp.route('/crear-productos')
@login_required
def crear_productos():
    return render_template('crear-productos.html')

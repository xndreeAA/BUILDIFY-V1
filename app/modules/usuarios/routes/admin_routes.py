from flask import Blueprint, jsonify, render_template, request, abort
from flask_login import login_required, current_user
import os
    
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates/admin')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static/admin')

admin_routes_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder=template_dir, 
    static_folder=static_dir
)

@admin_routes_bp.route('/')
@login_required  
def dashboard():
    return render_template('home.html', nombre=current_user.nombre)

@admin_routes_bp.route('/usuarios')
@login_required
def crud_usuarios():
    return render_template('crud-usuarios.html')




from flask import Blueprint, jsonify, render_template, request, abort
from flask_login import login_required, current_user
from app.core.models.rol import Rol 
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

@admin_routes_bp.route('/crud-usuarios')
@login_required
def crud_usuarios():
    return render_template('crud_usuarios.html')


@admin_routes_bp.route('/crear_usuarios')
@login_required
def crear_usuarios():
    roles = Rol.query.all()   
    return render_template('crear_usuarios.html', roles=roles)

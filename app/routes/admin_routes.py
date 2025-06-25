from flask import Blueprint, jsonify, render_template, request, abort
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
# @login_required  
def dashboard():
    return render_template('admin/home.html', nombre=current_user.nombre)

@admin_bp.route('/productos')
# @login_required
def crud_productos():
    return render_template('admin/crud-productos.html')


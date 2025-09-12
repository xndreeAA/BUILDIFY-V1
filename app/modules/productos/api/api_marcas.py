from flask import Blueprint, jsonify, request, abort
from flask_login import login_required

# ... otras importaciones necesarias
from app.modules.productos.controller.marca_controller import MarcasController

# Declara el Blueprint una sola vez
marcas_bp = Blueprint('api_marcas', __name__, url_prefix='/marcas')

marcas_bp.add_url_rule('/', view_func=MarcasController.handle_marcas, methods=['GET', 'POST'])
marcas_bp.add_url_rule('/<int:id_marca>', view_func=MarcasController.handle_marca_by_id, methods=['GET', 'PUT', 'DELETE'])
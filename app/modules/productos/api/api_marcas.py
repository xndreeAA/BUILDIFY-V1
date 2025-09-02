from flask import Blueprint, jsonify, request, abort
from flask_login import login_required

from app.modules.productos.models import Marca
from app import db

marcas_bp = Blueprint('api_marcas', __name__, url_prefix='/marcas')

from flask import Blueprint
from app.modules.productos.controller.marca_controller import MarcasController

marcas_bp = Blueprint('api_marcas', __name__, url_prefix='/marcas')

marcas_bp.add_url_rule('/', view_func=MarcasController.handle_marcas, methods=['GET', 'POST'])
marcas_bp.add_url_rule('/<int:id_marca>', view_func=MarcasController.handle_marca_by_id, methods=['GET', 'PUT', 'DELETE'])
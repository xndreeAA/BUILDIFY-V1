from flask import Blueprint
from app.modules.productos.controller.categoria_controller import CategoriasController

categorias_bp = Blueprint('api_categorias', __name__, url_prefix='/categorias')

categorias_bp.add_url_rule('/', view_func=CategoriasController.handle_categorias, methods=['GET', 'POST'])
categorias_bp.add_url_rule('/<int:id_categoria>', view_func=CategoriasController.handle_categoria_by_id, methods=['GET', 'PUT', 'DELETE'])

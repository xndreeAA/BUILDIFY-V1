from flask import Blueprint
from app.modules.landing.controller.carrusel_controller import CarruselController

#Blueprint para el módulo carrusel
carrusel_bp = Blueprint("carrusel_bp", __name__, url_prefix="/carrusel")

# Rutas principales
carrusel_bp.add_url_rule('/', view_func=CarruselController.obtener_items, methods=['GET'])
carrusel_bp.add_url_rule('/', view_func=CarruselController.crear_item, methods=['POST'])
carrusel_bp.add_url_rule('/<int:id_carrusel>', view_func=CarruselController.traer_un_item, methods=['GET'])
carrusel_bp.add_url_rule('/<int:id_carrusel>', view_func=CarruselController.modificar_item, methods=['PUT'])
carrusel_bp.add_url_rule('/<int:id_carrusel>', view_func=CarruselController.eliminar_item, methods=['DELETE'])

# Ruta especial para subir imagen a cloudinary
carrusel_bp.add_url_rule('/upload', view_func=CarruselController.subir_imagen, methods=['POST'])

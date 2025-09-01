from flask import Blueprint
from app.modules.usuarios.controller.usuario_controller import UsuarioController

usuarios_api_bp = Blueprint('api_usuarios', __name__, url_prefix='/usuarios')
usuarios_api_bp.add_url_rule('/current_user', view_func=UsuarioController.obtener_current_user, methods=['GET'])
usuarios_api_bp.add_url_rule('/', view_func=UsuarioController.obtener_usuarios, methods=['GET'])
usuarios_api_bp.add_url_rule("/", view_func=UsuarioController.crear_usuario, methods=["POST"])
usuarios_api_bp.add_url_rule("/<int:id_usuario>", view_func=UsuarioController.traer_un_usuario, methods=["GET"])
usuarios_api_bp.add_url_rule("/<int:id_usuario>", view_func=UsuarioController.modificar_un_usuario, methods=["PUT"])
usuarios_api_bp.add_url_rule("/<int:id_usuario>", view_func=UsuarioController.eliminar_un_usuario, methods=["DELETE"])

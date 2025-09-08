from flask import jsonify, abort, request
from app.modules.usuarios.services.usuario_service import UsuarioService

class UsuarioController:

    @staticmethod
    def obtener_current_user(*args, **kwargs):
        data, status = UsuarioService.obtener_current_user()
        return jsonify(data), status
    
    @staticmethod
    def obtener_usuarios(*args, **kwargs):
        data, status = UsuarioService.obtener_usuarios()
        return jsonify(data), status
    
    @staticmethod
    def crear_usuario(*args, **kwargs):
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        data, status = UsuarioService.crear_usuario(payload)

        return jsonify(data), status
    
    @staticmethod
    def traer_un_usuario(id_usuario, *args, **kwargs):
        data, status = UsuarioService.traer_un_usuario(id_usuario)

        return jsonify(data), status
    # Se elimina el parametro password en la modificacion de usuario
    @staticmethod
    def modificar_un_usuario(id_usuario, *args, **kwargs):
        
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos = ["nombre", "apellido", "email", "direccion", "telefono", "id_rol"]
        for campo in campos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        data, status = UsuarioService.modificar_un_usuario(id_usuario, payload)

        return jsonify(data), status
    
    @staticmethod
    def eliminar_un_usuario(id_usuario, *args, **kwargs):
        data, status = UsuarioService.eliminar_un_usuario(id_usuario)

        return jsonify(data), status
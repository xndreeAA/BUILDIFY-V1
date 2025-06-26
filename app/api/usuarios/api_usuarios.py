from flask import Blueprint, jsonify, request, abort
from flask_login import login_required

from app.models.usuario import Usuario
from app import db

user_api_bp = Blueprint('api_usuarios', __name__, url_prefix='/api/usuarios')

@user_api_bp.route('/', methods=['GET', 'POST'])
def api_usuarios():
    if request.method == 'GET':
        usuarios = Usuario.query.all()
        usuarios_data = [
            {
                "id_usuario": u.id_usuario,
                "nombre": u.nombre,
                "apellido": u.apellido,
                "email": u.email,
                "direccion": u.direccion,
                "telefono": u.telefono,
                "id_rol": u.id_rol,
                "password": u.password
            } for u in usuarios
        ]
        return jsonify({"success": True, "data": usuarios_data})

    elif request.method == 'POST':
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        nuevo_usuario = Usuario(**payload)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"success": True, "data": { "id_usuario": nuevo_usuario.id_usuario }})


@user_api_bp.route('/<int:id_usuario>', methods=['GET', 'PUT', 'DELETE'])
def api_usuario_individual(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario, description="Usuario no encontrado.")

    if request.method == 'GET':
        return jsonify({
            "success": True,
            "data": {
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "direccion": usuario.direccion,
                "telefono": usuario.telefono,
                "id_rol": usuario.id_rol,
                "password": usuario.password
            }
        })

    elif request.method == 'PUT':
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos = ["nombre", "apellido", "email", "direccion", "telefono", "id_rol", "password"]
        for campo in campos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        usuario.nombre = payload["nombre"]
        usuario.apellido = payload["apellido"]
        usuario.email = payload["email"]
        usuario.direccion = payload["direccion"]
        usuario.telefono = payload["telefono"]
        usuario.id_rol = payload["id_rol"]
        usuario.password = payload["password"]

        db.session.commit()
        return jsonify({ "success": True })

    elif request.method == 'DELETE':
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({ "success": True, "data": { "id_usuario": id_usuario }})

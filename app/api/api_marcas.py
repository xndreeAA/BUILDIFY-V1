from flask import Blueprint, jsonify, request, abort
from flask_login import login_required

from app.models.producto import Marca
from app import db

marcas_bp = Blueprint('api_marcas', __name__, url_prefix='/api/marcas')

@marcas_bp.route('/', methods=['GET', 'POST'])
def get_marcas():

    if request.method == 'GET':
        marcas = Marca.query.all()

        data = [
            { "id_marca": m.id_marca, "nombre": m.nombre } 
            for m in marcas
        ]
        return jsonify({"success": True, "data": data})
    
    elif request.method == 'POST':
        payload = request.get_json(silent=True)

        if not payload or not payload.get("nombre"):
            abort(400, description="El campo 'nombre' es obligatorio.")
        
        new_marca = Marca(nombre=payload["nombre"])
        db.session.add(new_marca)
        db.session.commit()

        return jsonify({
            "success": True, 
            "data": {"id_marca": new_marca.id_marca, "nombre": new_marca.nombre}
        })


@marcas_bp.route('/<int:id_marca>', methods=['GET', 'PUT', 'DELETE'])
def marca_id_operaciones(id_marca):
    marca = Marca.query.get_or_404(id_marca, description="Marca no encontrada.")

    if request.method == 'GET':
        return jsonify({
            "success": True,
            "data": { "id_marca": marca.id_marca, "nombre": marca.nombre }
        })

    elif request.method == 'DELETE':
        db.session.delete(marca)
        db.session.commit()
        return jsonify({ "success": True })

    elif request.method == 'PUT':
        payload = request.get_json(silent=True)
        
        if not payload:
            abort(400, description="Request body debe ser JSON valido.")

        marca.nombre = payload.get("nombre")
        db.session.commit()

        return jsonify({
            "success": True,
            "data": { "id_marca": marca.id_marca, "nombre": marca.nombre }
        })
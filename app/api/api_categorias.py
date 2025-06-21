from flask import Blueprint, jsonify, request, abort
from flask_login import login_required

from app.models.producto import Categoria
from app import db

categorias_bp = Blueprint('api_categorias', __name__, url_prefix='/api/categorias')

@categorias_bp.route('/', methods=['GET', 'POST'])
def get_categorias():

    if request.method == 'GET':
        categorias = Categoria.query.all()

        data = [
            { "id_categoria": c.id_categoria, "nombre": c.nombre } 
            for c in categorias
        ]
        return jsonify({"success": True, "data": data})
    
    elif request.method == 'POST':
        payload = request.get_json(silent=True)

        if not payload or not payload.get("nombre"):
            abort(400, description="El campo 'nombre' es obligatorio.")

        new_categoria = Categoria(nombre=payload["nombre"])
        db.session.add(new_categoria)
        db.session.commit()

        return jsonify({
            "success": True, 
            "data": {"id_categoria": new_categoria.id_categoria, "nombre": new_categoria.nombre}
        })

    else:
        abort(400, description="Metodo no permitido.")


@categorias_bp.route('/<int:id_categoria>', methods=['GET', 'PUT', 'DELETE'])
def categoria_id_operaciones(id_categoria):
    
    categoria = Categoria.query.get_or_404(id_categoria, description="Categoria no encontrada. ")

    if request.method == 'GET':
        return jsonify({
            "success": True,
            "data": { "id_categoria": categoria.id_categoria, "nombre": categoria.nombre }
        })

    elif request.method == 'DELETE':
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({ "success": True })

    elif request.method == 'PUT':
        payload = request.get_json(silent=True)
        
        if not payload:
            abort(400, description="Request body debe ser JSON valido.")

        categoria.nombre = payload.get("nombre")
        db.session.commit()

        return jsonify({
            "success": True,
            "data": { "id_categoria": categoria.id_categoria, "nombre": categoria.nombre }
        })

from flask import Blueprint, jsonify, request, abort
from flask_login import login_required

from app.models.producto import Producto
from app import db

productos_bp = Blueprint('api_productos', __name__, url_prefix='/api/productos')

@productos_bp.route('/', methods=['GET', 'POST'])
# @login_required
def api_productos():
    if request.method == 'GET':
        productos = Producto.query.all()

        productos_data = [
            {
                "id_producto": p.id_producto,
                "nombre": p.nombre,
                "precio": float(p.precio),
                "stock": p.stock,
                "id_categoria": p.id_categoria,
                "id_marca": p.id_marca,
                "imagen": p.imagen
            } for p in productos
        ]

        return jsonify({ "success": True, "data": productos_data })

    elif request.method == 'POST':
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos = ["nombre", "precio", "stock", "id_categoria", "id_marca", "imagen"]
        for campo in campos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        nuevo_producto = Producto(
            nombre=payload["nombre"],
            precio=payload["precio"],
            stock=payload["stock"],
            id_categoria=payload["id_categoria"],
            id_marca=payload["id_marca"],
            imagen=payload["imagen"]
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        return jsonify({ "success": True, "id_producto": nuevo_producto.id_producto }), 201

    else:
        abort(405, description="Método no permitido.")


@productos_bp.route('/<int:id_producto>', methods=['GET', 'DELETE', 'PUT'])
def producto_id_operaciones(id_producto):
    producto = Producto.query.get_or_404(id_producto, description="Producto no encontrado.")

    if request.method == 'GET':
        return jsonify({
            "success": True,
            "data": {
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "stock": producto.stock,
                "id_categoria": producto.id_categoria,
                "id_marca": producto.id_marca,
                "imagen": producto.imagen
            }
        })

    elif request.method == 'DELETE':
        db.session.delete(producto)
        db.session.commit()
        return jsonify({ "success": True })

    elif request.method == 'PUT':
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos = ["nombre", "precio", "stock", "id_categoria", "id_marca", "imagen"]
        for campo in campos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        producto.nombre = payload["nombre"]
        producto.precio = payload["precio"]
        producto.stock = payload["stock"]
        producto.id_categoria = payload["id_categoria"]
        producto.id_marca = payload["id_marca"]
        producto.imagen = payload["imagen"]

        db.session.commit()
        return jsonify({ "success": True })

    else:
        abort(405, description="Método no permitido.")


@productos_bp.route('/all', methods=['GET'])
def api_productos_all():
    productos = Producto.query.options(
        db.joinedload(Producto.categoria),
        db.joinedload(Producto.marca)
    ).all()
    
    productos_data = []
    for producto in productos:
        productos_data.append({
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "precio": float(producto.precio),
            "stock": producto.stock,
            "categoria": producto.categoria.nombre,  
            "marca": producto.marca.nombre
        })
    
    return jsonify(productos_data)
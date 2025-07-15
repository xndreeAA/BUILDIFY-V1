from flask import Blueprint, jsonify, request, abort
from app import db
from app.models.carrito import Carrito, ItemCarrito
from app.models.usuario import Usuario
from app.models.producto import Producto
from sqlalchemy.orm import joinedload

carrito_bp = Blueprint('api_carrito', __name__, url_prefix='/api/carrito')

@carrito_bp.route('/<int:id_usuario>', methods=['GET'])
def obtener_carrito(id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario, description="Usuario no encontrado.")
        carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
        if not carrito:
            carrito = Carrito(id_usuario=id_usuario)
            db.session.add(carrito)
            db.session.commit()

        items = ItemCarrito.query.options(
            joinedload(ItemCarrito.producto).joinedload(Producto.imagenes),
            joinedload(ItemCarrito.producto).joinedload(Producto.categoria),
            joinedload(ItemCarrito.producto).joinedload(Producto.marca)
        ).filter_by(id_carrito=carrito.id_carrito).all()

        items_serializados = [item.to_dict() for item in items]

        return jsonify({
            "success": True,
            "carrito": {
                "id_carrito": carrito.id_carrito,
                "items": items_serializados,
                "total": float(sum(item.producto.precio * item.cantidad for item in items))
            }
        })

@carrito_bp.route('/', methods=['POST'])
def actualizar_carrito():
    payload = request.get_json(silent=True)
    if not payload:
        abort(400, description="Request body debe ser JSON válido")

    campos_requeridos = ["id_usuario", "id_producto", "cantidad"]
    for campo in campos_requeridos:
        if campo not in payload:
            abort(400, description=f"Falta el campo requerido: {campo}")

    carrito = Carrito.query.filter_by(id_usuario=payload["id_usuario"]).first()
    if not carrito:
        carrito = Carrito(id_usuario=payload["id_usuario"])
        db.session.add(carrito)
        db.session.commit()

    producto = Producto.query.get_or_404(payload["id_producto"], description="Producto no encontrado.")

    cantidad = payload["cantidad"]
    if not isinstance(cantidad, int) or cantidad <= 0:
        abort(400, description="La cantidad debe ser un número entero positivo.")
    elif cantidad > producto.stock:
        abort(400, description="La cantidad excede el stock disponible.")

    item_existente = ItemCarrito.query.filter_by(
        id_carrito=carrito.id_carrito,
        id_producto=producto.id_producto
    ).first()

    if item_existente:
        return jsonify({
            "success": False,
            "error": "El producto ya estaba en el carrito."
        }), 409
    else:
        nuevo_item = ItemCarrito(
            id_carrito=carrito.id_carrito,
            id_producto=producto.id_producto,
            cantidad=cantidad
        )
        db.session.add(nuevo_item)

    db.session.commit()

    return jsonify({
        "success": True,
        "item": (nuevo_item).to_dict()
    }), 201


@carrito_bp.route('/', methods=['PUT'])
def modificar_cantidad_producto_carrito():
    payload = request.get_json(silent=True)
    if not payload:
        abort(400, description="Request body debe ser JSON válido")

    campos_requeridos = ["id_usuario", "id_producto", "cantidad"]
    for campo in campos_requeridos:
        if campo not in payload:
            abort(400, description=f"Falta el campo requerido: {campo}")

    carrito = Carrito.query.filter_by(id_usuario=payload["id_usuario"]).first()
    if not carrito:
        return jsonify({
            "success": False,
            "error": "El carrito no existe."
        }), 404

    producto = Producto.query.get_or_404(payload["id_producto"], description="Producto no encontrado.")

    item_carrito = ItemCarrito.query.filter_by(
        id_carrito=carrito.id_carrito,
        id_producto=producto.id_producto
    ).first()

    if not item_carrito:
        return jsonify({
            "success": False,
            "error": "El producto no estaba en el carrito."
        }), 404

    cantidad = payload["cantidad"]
    if not isinstance(cantidad, int) or cantidad <= 0:  
        abort(400, description="La cantidad debe ser un número entero positivo.")
    elif cantidad > producto.stock:
        abort(400, description="La cantidad excede el stock disponible.")
    if cantidad == 0:
        db.session.delete(item_carrito)
        db.session.commit()
        return jsonify({"success": True, "removed": True}), 200
    
    item_carrito.cantidad = cantidad
    db.session.commit()

    return jsonify({
        "success": True,
        "item": item_carrito.to_dict()
    }), 200

@carrito_bp.route('/', methods=['DELETE'])
def eliminar_producto_carrito():
    payload = request.get_json(silent=True)
    if not payload:
        abort(400, description="Request body debe ser JSON válido")

    campos_requeridos = ["id_usuario", "id_producto"]
    for campo in campos_requeridos:
        if campo not in payload:
            abort(400, description=f"Falta el campo requerido: {campo}")

    carrito = Carrito.query.filter_by(id_usuario=payload["id_usuario"]).first()
    if not carrito:
        return jsonify({
            "success": False,
            "error": "El carrito no existe."
        }), 404

    producto = Producto.query.get_or_404(payload["id_producto"], description="Producto no encontrado.")

    item_carrito = ItemCarrito.query.filter_by(
        id_carrito=carrito.id_carrito,
        id_producto=producto.id_producto
    ).first()

    if not item_carrito:
        return jsonify({
            "success": False,
            "error": "El producto no estaba en el carrito."
        }), 404

    db.session.delete(item_carrito)
    db.session.commit()

    return jsonify({
        "success": True,
        "item": item_carrito.to_dict()
    }), 200
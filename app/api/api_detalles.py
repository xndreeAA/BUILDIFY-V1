from flask import Blueprint, jsonify, request, abort
from flask_login import login_required

from app.models.producto import Producto
from app import db

detalles_bp = Blueprint('api_detalles', __name__, url_prefix='/api/detalles')

@detalles_bp.route('/<int:id_producto>', methods=['GET'])
def detalles_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto, description="Producto no encontrado.")
    
    resultado = {
        "id_producto": producto.id_producto,
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "stock": producto.stock,
        "id_categoria": producto.id_categoria,
        "id_marca": producto.id_marca,
        "imagen": producto.imagen
    }
    
    return jsonify(producto.detalles)
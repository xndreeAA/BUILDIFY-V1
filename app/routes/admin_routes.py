from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user

from app.models.producto import Producto
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required  
def dashboard():
    return render_template('admin/home.html', nombre=current_user.nombre)

@admin_bp.route('/productos')
@login_required
def crud_productos():
    return render_template('admin/crud-productos.html')

@admin_bp.route('/api/productos')
@login_required
def api_productos():
    productos = Producto.query.options(
        db.joinedload(Producto.categoria),
        db.joinedload(Producto.marca)
    ).all()
    
    productos_data = []
    for producto in productos:
        productos_data.append({
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "precio": float(producto.precio),  # Convert Decimal to float
            "stock": producto.stock,
            "categoria": producto.categoria.nombre,  # Get category name
            "marca": producto.marca.nombre  # Get brand name
            # "imagen": producto.imagen
        })
    
    return jsonify(productos_data)
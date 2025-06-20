from flask import Blueprint, jsonify, render_template, request, abort
from flask_login import login_required, current_user

from sqlalchemy.orm import joinedload

from app.models.producto import Producto, Categoria, Marca
from app.models.detalles_producto import DetalleChasis, DetallePlacaBase, DetalleMemoriaRAM, DetalleFuentePoder, DetalleProcesador, DetalleRefrigeracion, DetalleTarjetaGrafica
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required  
def dashboard(): #cambiar
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

def get_detalles_por_categoria(id_producto: int, nombre_categoria: str):
    # Normalizamos la cadena
    nc = nombre_categoria.strip().lower()
    match nc:
        case "chasises":
            return (
                db.session
                  .query(DetalleChasis)
                  .filter(DetalleChasis.id_producto == id_producto)
                  .first_or_404(description="No se hallaron detalles de chasis.")
            )
        case "fuentes de poder":
            return (
                db.session
                  .query(DetalleFuentePoder)
                  .filter(DetalleFuentePoder.id_producto == id_producto)
                  .first_or_404(description="No se hallaron detalles de fuente de poder.")
            )
        case "memorias ram":
            return (
                db.session
                  .query(DetalleMemoriaRAM)
                  .filter(DetalleMemoriaRAM.id_producto == id_producto)
                  .first_or_404(description="No se hallaron detalles de memoria RAM.")
            )
        case "placas base":
            return (
                db.session
                  .query(DetallePlacaBase)
                  .filter(DetallePlacaBase.id_producto == id_producto)
                  .first_or_404(description="No se hallaron detalles de placa base.")
            )
        case "procesadores":
            return (
                db.session
                  .query(DetalleProcesador)
                  .filter(DetalleProcesador.id_producto == id_producto)
                  .first_or_404(description="No se hallaron detalles de procesador.")
            )
        case "refrigeraciones":
            return (
                db.session
                  .query(DetalleRefrigeracion)
                  .filter(DetalleRefrigeracion.id_producto == id_producto)
                  .first_or_404(description="No se hallaron detalles de refrigeración.")
            )
        case "tarjetas graficas":
            return (
                db.session
                  .query(DetalleTarjetaGrafica)
                  .filter(DetalleTarjetaGrafica.id_producto == id_producto)
                  .first_or_404(description="No se hallaron detalles de tarjeta gráfica.")
            )
        case _:
            abort(400, description=f"Categoría '{nombre_categoria}' no soportada para detalles.")

@admin_bp.route('/api/productos/detalles')
@login_required
def api_producto_con_detalles():
    # 1) Leer parámetros
    id_producto = request.args.get('id_producto', type=int)
    nombre_cat = request.args.get('categoria', type=str)

    if id_producto is None or not nombre_cat:
        abort(400, description="Faltan parámetros: 'id_producto' y 'categoria' son requeridos.")

    # 2) Traer producto con sus relaciones básicas
    producto = (
        db.session.query(Producto)
        .join(Categoria)
        .join(Marca)
        .options(
            db.joinedload(Producto.categoria),
            db.joinedload(Producto.marca)
        )
        .filter(
            Producto.id_producto == id_producto,
            Categoria.nombre.ilike(nombre_cat.strip())
        )
        .first_or_404(description="No se encontró el producto.")
    )

    # 3) Obtener el objeto de detalles específico
    detalles_obj = get_detalles_por_categoria(id_producto, producto.categoria.nombre)

    # 4) Armar la respuesta JSON
    resultado = {
        "id_producto": producto.id_producto,
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "stock": producto.stock,
        "imagen": producto.imagen,
        "categoria": {
            "id_categoria": producto.categoria.id_categoria,
            "nombre": producto.categoria.nombre
        },
        "marca": {
            "id_marca": producto.marca.id_marca,
            "nombre": producto.marca.nombre
        },
        # Serializamos los detalles de forma manual y explícita
        "detalles": {
            k: v
            for k, v in detalles_obj.__dict__.items()
            if not k.startswith("_sa_instance_state")
        }
    }
    return jsonify(resultado), 200

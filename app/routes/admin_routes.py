from flask import Blueprint, jsonify, render_template, request, abort
from flask_login import login_required, current_user

from sqlalchemy.orm import joinedload

from app.models.producto import Producto, Categoria, Marca
from app.models.detalles_producto import DetalleChasis, DetallePlacaBase, DetalleMemoriaRAM, DetalleFuentePoder, DetalleProcesador, DetalleRefrigeracion, DetalleTarjetaGrafica
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
# @login_required  
def dashboard():
    return render_template('admin/home.html', nombre=current_user.nombre)

@admin_bp.route('/productos')
# @login_required
def crud_productos():
    return render_template('admin/crud-productos.html')

@admin_bp.route('/api/productos')
# @login_required
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
# @login_required
def api_producto_con_detalles():
    id_producto = request.args.get('id_producto', type=int)
    nombre_cat = request.args.get('categoria', type=str)

    if id_producto is None or not nombre_cat:
        abort(400, description="Faltan parámetros: 'id_producto' y 'categoria' son requeridos.")

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

    detalles_obj = get_detalles_por_categoria(id_producto, producto.categoria.nombre)

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

@admin_bp.route('/api/productos/<int:id_producto>', methods=['PUT'])
# @login_required
def api_producto_actualizar(id_producto):
    # 1) Leer y validar el JSON entrante
    payload = request.get_json(silent=True)
    if not payload:
        abort(400, description="Request body debe ser JSON válido.")

    nombre      = payload.get("nombre")
    precio      = payload.get("precio")
    stock       = payload.get("stock")
    imagen      = payload.get("imagen")
    categoria_j = payload.get("categoria", {}).get("nombre")
    marca_j     = payload.get("marca", {}).get("nombre")
    detalles_j  = payload.get("detalles", {})

    # Asegura que vengan al menos los campos básicos
    if nombre is None or precio is None or stock is None:
        abort(400, description="Faltan campos obligatorios: 'nombre', 'precio' y 'stock'.")

    # 2) Buscar el producto existente
    producto = Producto.query.get_or_404(id_producto, description="Producto no encontrado.")

    # 3) Actualizar campos en la tabla productos
    producto.nombre = nombre
    producto.precio = precio
    producto.stock  = stock
    producto.imagen = imagen

    # Si te interesa también permitir cambiar categoría y marca:
    if categoria_j:
        cat = Categoria.query.filter_by(nombre=categoria_j).first()
        if not cat:
            abort(400, description=f"Categoría '{categoria_j}' no existe.")
        producto.id_categoria = cat.id_categoria

    if marca_j:
        mar = Marca.query.filter_by(nombre=marca_j).first()
        if not mar:
            abort(400, description=f"Marca '{marca_j}' no existe.")
        producto.id_marca = mar.id_marca

    # 4) Obtener el objeto de detalles según la categoría actual
    detalles_obj = get_detalles_por_categoria(producto.id_producto, producto.categoria.nombre)

    # 5) Recorrer y asignar cada campo de detalles
    for campo, valor in detalles_j.items():
        if hasattr(detalles_obj, campo):
            setattr(detalles_obj, campo, valor)
        else:
            # Ignora claves inesperadas o aborta si prefieres ser estricto
            abort(400, description=f"Campo de detalle inválido: '{campo}'.")

    # 6) Confirmar cambios en la base
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description="Error al guardar los cambios.")

    # 7) Devolver el recurso actualizado (puedes reutilizar tu serialización)
    salida = {
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
        "detalles": {
            k: v
            for k, v in detalles_obj.__dict__.items()
            if not k.startswith("_sa_instance_state")
        }
    }
    return jsonify(salida), 200



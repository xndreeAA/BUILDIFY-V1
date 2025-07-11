from flask import Blueprint, jsonify, request, abort, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.models.producto import Producto, ImagenesProducto
from app.models.detalles_producto import (
    DetalleChasis, DetalleFuentePoder, DetalleMemoriaRAM,
    DetallePlacaBase, DetalleProcesador, DetalleRefrigeracion,
    DetalleTarjetaGrafica
)
from app import db
import os
import traceback

productos_bp = Blueprint('api_productos', __name__, url_prefix='/api/productos')

MAPA_DETALLES = {
    1: DetalleProcesador,
    2: DetalleMemoriaRAM,
    3: DetalleTarjetaGrafica,
    4: DetalleChasis,
    5: DetalleRefrigeracion,
    6: DetalleFuentePoder,
    7: DetallePlacaBase,
}

@productos_bp.route('/', methods=['GET', 'POST'])
# @login_required
def api_productos():
    if request.method == 'GET':
        
        productos = Producto.query.options(
            db.joinedload(Producto.categoria),
            db.joinedload(Producto.marca),
            db.joinedload(Producto.imagenes)
        ).all()
        
        productos_data = []

        for producto in productos:
            productos_data.append({
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "stock": producto.stock,
                "categoria": producto.categoria.nombre,  
                "marca": producto.marca.nombre,
                "imagenes": [
                    {
                        "ruta": imagen.nombre_archivo,
                        "es_principal": imagen.es_principal
                    }
                    for imagen in producto.imagenes
                ]
            })
        
        return jsonify({ "success": True, "data": productos_data })
    elif request.method == 'POST':
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos_requeridos = ["nombre", "precio", "stock", "id_marca", "id_categoria", "detalles"]
        for campo in campos_requeridos:
            if campo not in payload:
                abort(400, description=f"Falta el campo obligatorio: {campo}")

        nuevo_producto = Producto(
            nombre=payload["nombre"],
            precio=payload["precio"],
            stock=payload["stock"],
            id_marca=payload["id_marca"],
            id_categoria=payload["id_categoria"]
        )

        db.session.add(nuevo_producto)
        db.session.flush()

        modelo_detalle = MAPA_DETALLES.get(payload["id_categoria"])
        if modelo_detalle:
            detalles_payload = payload["detalles"]
            detalle = modelo_detalle(id_producto=nuevo_producto.id_producto, **detalles_payload)
            db.session.add(detalle)

        for imagen in payload.get("imagenes", []):
            nueva_imagen = ImagenesProducto(
                id_producto=nuevo_producto.id_producto,
                nombre_archivo=imagen["ruta"],
                es_principal=imagen["es_principal"]
            )
            db.session.add(nueva_imagen)

        db.session.commit()

        return jsonify({ "success": True, "data": { "id_producto": nuevo_producto.id_producto } }), 201
    else:
        abort(405, description="Método no permitido.")

@productos_bp.route('/<int:id_producto>', methods=['GET', 'DELETE', 'PUT'])
def producto_id_operaciones(id_producto):
    if request.method == 'GET':
        producto = Producto.query.get_or_404(id_producto, description="Producto no encontrado.")
        return jsonify({
            "success": True,
            "data": {
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "stock": producto.stock,
                "id_categoria": producto.id_categoria,
                "id_marca": producto.id_marca,
                "imagenes": [
                    {
                        "ruta": imagen.nombre_archivo,
                        "es_principal": imagen.es_principal
                    }
                    for imagen in producto.imagenes
                ]
            }
        })

    elif request.method == 'DELETE':
        try:
            producto = Producto.query.get_or_404(id_producto, description="Producto no encontrado.")
            print(f"🟠 Intentando eliminar el producto ID {id_producto}")

            db.session.delete(producto)
            db.session.commit()
            print("✅ Producto eliminado correctamente")
            return jsonify({ "success": True })
        except Exception as e:
            db.session.rollback()
            print("🔥 ERROR AL ELIMINAR PRODUCTO:")
            traceback.print_exc()
            return jsonify({ 
                "success": False, 
                "error": str(e), 
                "tipo": type(e).__name__ 
            }), 400

    elif request.method == 'PUT':
        producto = Producto.query.get_or_404(id_producto, description="Producto no encontrado.")
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos = ["nombre", "precio", "stock", "id_categoria", "id_marca"]
        for campo in campos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        producto.nombre = payload["nombre"]
        producto.precio = payload["precio"]
        producto.stock = payload["stock"]
        producto.id_categoria = payload["id_categoria"]
        producto.id_marca = payload["id_marca"]

        db.session.commit()
        return jsonify({ "success": True })

    else:
        abort(405, description="Método no permitido.")
        
        


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@productos_bp.route('/subir-imagen', methods=['POST'])
def subir_imagen():
    imagenes = request.files.getlist('imagenes')
    id_producto = request.form.get('id_producto')
    categoria = request.form.get('categoria')
    principales = request.form.getlist('es_principal')

    if not imagenes or not id_producto or not categoria:
        abort(400, description="Faltan datos requeridos.")

    base_path = os.path.join(current_app.root_path, 'static', 'images', categoria, f'producto_{id_producto}')
    os.makedirs(base_path, exist_ok=True)

    rutas = []
    from app.models.producto import ImagenesProducto

    for idx, imagen in enumerate(imagenes):
        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            ruta_relativa = f'images/{categoria}/producto_{id_producto}/{filename}'
            ruta_absoluta = os.path.join(base_path, filename)
            imagen.save(ruta_absoluta)

            imagen_db = ImagenesProducto(
                nombre_archivo=ruta_relativa,
                es_principal=(principales[idx].lower() == 'true'),
                id_producto=int(id_producto)
            )
            db.session.add(imagen_db)
            rutas.append(ruta_relativa)
        else:
            abort(400, description="Archivo no válido.")

    db.session.commit()

    return jsonify({
        "success": True,
        "imagenes_guardadas": rutas
    })
# ------------------------------------------------------------------------------------------------

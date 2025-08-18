from flask import Blueprint, jsonify, request, abort, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from sqlalchemy import or_
import cloudinary
import cloudinary.uploader

from app.modules.productos.models import (
    Producto, Categoria, Marca, ImagenesProducto,
    DetalleChasis, DetalleFuentePoder, DetalleMemoriaRAM,
    DetallePlacaBase, DetalleProcesador, DetalleRefrigeracion,
    DetalleTarjetaGrafica
)

from app import db
import os
import traceback
import shutil

productos_bp = Blueprint('api_productos', __name__, url_prefix='/productos')

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
def api_productos():
    if request.method == 'GET':
        busqueda = request.args.get('busqueda')
        categoria_nombre = request.args.get('categoria')
        if categoria_nombre:
            categoria_nombre = categoria_nombre.lower()
        marca_nombre = request.args.get('marca')
        if marca_nombre:
            marca_nombre = marca_nombre.lower()

        query = Producto.query.options(
            db.joinedload(Producto.categoria),
            db.joinedload(Producto.marca),
            db.joinedload(Producto.imagenes)
        )
        if busqueda:
            query = query.join(Producto.categoria).filter(
                or_(
                    Producto.nombre.ilike(f"%{busqueda}%"),
                    Categoria.nombre.ilike(f"%{busqueda}%"),
                    Marca.nombre.ilike(f"%{busqueda}%")
                )
            )
        if marca_nombre:
            query = query.join(Producto.marca).filter(Marca.nombre == marca_nombre)
        if categoria_nombre:
            query = query.join(Producto.categoria).filter(Categoria.nombre == categoria_nombre)

        productos = query.all()
        productos_data = [producto.to_dict() for producto in productos]

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

            categoria = producto.categoria.nombre
            folder_path =  os.path.join(current_app.root_path, 'static', 'images', categoria, f'producto_{id_producto}')

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                print(f"🧹 Carpeta de imágenes eliminada: {folder_path}")
            else:
                print(f"⚠️ Carpeta de imágenes no encontrada: {folder_path}. Omitiendo...")

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
    
    cloudinary.config(
        cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=current_app.config.get("CLOUDINARY_API_KEY"),
        api_secret=current_app.config.get("CLOUDINARY_API_SECRET")
    )

    imagenes = request.files.getlist('imagenes')
    id_producto = request.form.get('id_producto')
    categoria = request.form.get('categoria')
    principales = request.form.getlist('es_principal')

    if not imagenes or not id_producto or not categoria:
        abort(400, description="Faltan datos requeridos.")

    base_path = os.path.join(current_app.root_path, 'static', 'images', categoria, f'producto_{id_producto}')
    os.makedirs(base_path, exist_ok=True)

    rutas = []

    for idx, imagen in enumerate(imagenes):
        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            
            if not filename:
                abort(400, description="Nombre de archivo no valido.")

            carpeta = f"buildify/productos/{categoria}/producto_{id_producto}"

            try:
                upload_result = cloudinary.uploader.upload(
                    imagen,
                    folder=carpeta,
                    use_filename=True,
                    unique_filename=False
                )
            except Exception as e:
                current_app.logger.error(f"Error al subir imagen: {e}")
                abort(500, description="Error al subir imagen a Cloudinary.")

            url = upload_result.get("secure_url")
            if not url:
                abort(500, description="No se pudo obtener la URL de Cloudinary.")

            imagen_db = ImagenesProducto(
                nombre_archivo=url,
                es_principal=(principales[idx].lower() == 'true'),
                id_producto=int(id_producto)
            )

            db.session.add(imagen_db)
            rutas.append(url)
        else:
            abort(400, description="Archivo no válido.")

    db.session.commit()

    return jsonify({
        "success": True,
        "imagenes_guardadas": rutas
    })
# ------------------------------------------------------------------------------------------------

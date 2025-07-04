from flask import Blueprint, request, jsonify, abort, current_app
from werkzeug.utils import secure_filename
import os

upload_bp = Blueprint('api_upload', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/subir-imagen', methods=['POST'])
def subir_imagen():
    imagenes = request.files.getlist('imagenes')
    id_producto = request.form.get('id_producto')
    categoria = request.form.get('categoria')
    principales = request.form.getlist('es_principal')

    if not imagenes or not id_producto or not categoria:
        abort(400, description="Faltan datos requeridos.")

    # Ruta: static/img/<categoria>/producto_<id_producto>/
    base_path = os.path.join(current_app.root_path, 'static', 'img', categoria, f'producto_{id_producto}')
    os.makedirs(base_path, exist_ok=True)

    rutas = []
    from app.models.producto import ImagenesProducto
    from app import db

    for idx, imagen in enumerate(imagenes):
        if imagen and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            ruta_relativa = f'img/{categoria}/producto_{id_producto}/{filename}'
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

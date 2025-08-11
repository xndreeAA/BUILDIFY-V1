from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import joinedload
from app.models.producto import Producto, ImagenesProducto
from app.models.detalles_producto import (
    DetalleChasis, DetalleFuentePoder, DetalleMemoriaRAM,
    DetallePlacaBase, DetalleProcesador, DetalleRefrigeracion,
    DetalleTarjetaGrafica
)
from app import db

detalles_bp = Blueprint('api_detalles', __name__, url_prefix='/api/detalles')

MAPA_DETALLES = {
    1: DetalleProcesador,
    2: DetalleMemoriaRAM,
    3: DetalleTarjetaGrafica,
    4: DetalleChasis,
    5: DetalleRefrigeracion,
    6: DetalleFuentePoder,
    7: DetallePlacaBase,
}

TIPOS_DEFAULT = {
    db.String: "text",
    db.Integer: "number",
    db.Boolean: "checkbox",
    db.Numeric: "number",
    db.Float: "number",
}

def convertir_tipo_seguro(modelo, field, value):
    column_type = getattr(modelo.__table__.columns, field).type
    if isinstance(column_type, db.Boolean):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', '1']
        if isinstance(value, int):
            return value == 1
        raise TypeError(f"Valor no válido para booleano: {value}")
    return value

@detalles_bp.route("/campos/<int:id_categoria>", methods=["GET"])
def obtener_campos_detalle(id_categoria):
    modelo = MAPA_DETALLES.get(id_categoria)
    if not modelo:
        return jsonify({"success": False, "error": "Categoría sin modelo de detalles asociado."}), 400

    campos = []
    for col in modelo.__table__.columns:
        if col.name == "id_producto":
            continue

        tipo_sqlalchemy = type(col.type)
        tipo_html = TIPOS_DEFAULT.get(tipo_sqlalchemy, "text")

        campos.append({
            "nombre": col.name,
            "tipo": tipo_html
        })

    return jsonify({ "success": True, "campos": campos })

@detalles_bp.route('/<int:id_producto>', methods=['GET', 'PUT', 'DELETE'])
def detalles_producto(id_producto):

    producto = (
        Producto.query
        .options(
            joinedload(Producto.marca),
            joinedload(Producto.categoria),
            joinedload(Producto.imagenes)
        )
        .filter_by(id_producto=id_producto)
        .first_or_404(description="Producto no encontrado.")
    )

    modelo_detalle = MAPA_DETALLES.get(producto.id_categoria)

    if request.method == 'GET':
        data = {
            "id_producto": producto.id_producto,
            "nombre": producto.nombre,
            "precio": float(producto.precio),
            "stock": producto.stock,
            "marca": {
                "id_marca": producto.marca.id_marca,
                "nombre": producto.marca.nombre
            },
            "categoria": {
                "id_categoria": producto.categoria.id_categoria,
                "nombre": producto.categoria.nombre
            },
            "imagenes": [
                {
                    "ruta": imagen.nombre_archivo,
                    "es_principal": imagen.es_principal
                }
                for imagen in producto.imagenes
            ],
            "detalles": None
        }

        if modelo_detalle:
            detalle = modelo_detalle.query.filter_by(id_producto=producto.id_producto).first()

            if detalle:
                detalle_dict = {
                    col.name: getattr(detalle, col.name)
                    for col in modelo_detalle.__table__.columns
                    if col.name != "id_producto"
                }

                for key, value in detalle_dict.items():
                    if isinstance(value, db.Numeric):
                        detalle_dict[key] = float(value)

                data["detalles"] = detalle_dict

        return jsonify({ "success": True, "data": data })

    elif request.method == 'PUT':
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request debe contener JSON válido.")

        for field in ['nombre', 'precio', 'stock', "id_marca", "id_categoria"]:
            if field in payload:
                setattr(producto, field, payload[field])

        if 'categoria' in payload:
            setattr(producto, 'id_categoria', payload['categoria'])

        if 'imagenes' in payload and isinstance(payload['imagenes'], list):
            ImagenesProducto.query.filter_by(id_producto=id_producto).delete()

            for imagen in payload['imagenes']:
                nueva_imagen = ImagenesProducto(
                    id_producto=id_producto,
                    nombre_archivo=imagen.get('ruta'),
                    es_principal=imagen.get('es_principal', False)
                )
                db.session.add(nueva_imagen)

        if modelo_detalle and 'detalles' in payload:
            detalle = modelo_detalle.query.filter_by(id_producto=id_producto).first()
            if detalle:
                for field, value in payload['detalles'].items():
                    if hasattr(detalle, field):
                        try:
                            setattr(detalle, field, convertir_tipo_seguro(modelo_detalle, field, value))
                        except TypeError as e:
                            abort(400, description=str(e))

        db.session.commit()
        return jsonify({ "success": True })

    elif request.method == 'DELETE':
        # 👇 CAMBIO AGREGADO: eliminar también los detalles si existen
        if modelo_detalle:
            detalle = modelo_detalle.query.filter_by(id_producto=id_producto).first()
            if detalle:
                db.session.delete(detalle)

        db.session.delete(producto)
        db.session.commit()
        return jsonify({ "success": True })

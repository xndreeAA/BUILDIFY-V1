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

@detalles_bp.route('/<int:id_producto>', methods=['GET', 'PUT', 'DELETE'])
def detalles_producto(id_producto):

    producto = (
        Producto.query
        .options(
            joinedload(Producto.marca),
            joinedload(Producto.categoria)
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
                        setattr(detalle, field, value)

        db.session.commit()
        return jsonify({ "success": True })
from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import joinedload
from app.models.producto import Producto
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
            "imagen": producto.imagen,
            "marca": {
                "id_marca": producto.marca.id_marca,
                "nombre": producto.marca.nombre
            },
            "categoria": {
                "id_categoria": producto.categoria.id_categoria,
                "nombre": producto.categoria.nombre
            },
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

        for field in ['nombre', 'precio', 'stock', 'imagen', "id_marca", "id_categoria"]:
            if field in payload:
                setattr(producto, field, payload[field])

        if 'categoria' in payload:
            setattr(producto, 'id_categoria', payload['categoria'])

        if modelo_detalle and 'detalles' in payload:
            detalle = modelo_detalle.query.filter_by(id_producto=id_producto).first()
            if detalle:
                for field, value in payload['detalles'].items():
                    if hasattr(detalle, field):
                        # 👇 CAMBIO AGREGADO: detectar si el campo es booleano
                        column_type = modelo_detalle.__table__.columns[field].type
                        if isinstance(column_type, db.Boolean):
                            # 👇 CAMBIO AGREGADO: convertir string 'false'/'true' a booleano real
                            if isinstance(value, str):
                                value = value.lower() == 'true'
                        setattr(detalle, field, value)

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

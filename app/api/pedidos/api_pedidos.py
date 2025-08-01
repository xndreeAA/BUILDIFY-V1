from flask import Blueprint, jsonify, request, abort, current_app
from flask_login import login_required
from sqlalchemy.orm import joinedload

from app.models.pedidos import Pedido, ProductoPedido, Estado
from app.models.usuario import Usuario
from app.models.producto import Producto, Categoria, Marca
from datetime import datetime
from collections import defaultdict
from app import db

pedidos_bp = Blueprint('api_pedidos', __name__, url_prefix='/api/pedidos')

@pedidos_bp.route('/', methods=['GET'])
def obtener_pedidos():
    
    mas_vendido = request.args.get('mas_vendido')
    menos_vendido = request.args.get('menos_vendido')
    mas_vendido_categoria = request.args.get('mas_vendido_categoria')
    menos_vendido_categoria = request.args.get('menos_vendido_categoria')
    mas_vendido_marca = request.args.get('mas_vendido_marca')
    menos_vendido_marca = request.args.get('menos_vendido_marca')
    mas_vendido_producto = request.args.get('mas_vendido_producto')
    menos_vendido_producto = request.args.get('menos_vendido_producto')

    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    formato = "%Y-%m-%d"
    param_producto = request.args.get('producto')
    param_categoria = request.args.get('categoria')
    param_marca = request.args.get('marca')
    param_estado = request.args.get('estado')

    query = Pedido.query.options(
        joinedload(Pedido.productos_pedidos).joinedload(ProductoPedido.producto),
        joinedload(Pedido.usuario),
        joinedload(Pedido.estado),
    )

    try:
        if fecha_desde:
            fecha_desde = datetime.strptime(fecha_desde, formato).date()
        if fecha_hasta:
            fecha_hasta = datetime.strptime(fecha_hasta, formato).date()
    except ValueError:
        return jsonify({
            "success": False, 
            "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
        }), 400

    if fecha_desde:
        query = query.filter(Pedido.fecha_pedido >= fecha_desde)

    if fecha_hasta:
        query = query.filter(Pedido.fecha_pedido <= fecha_hasta)

    if param_producto:
        query = query.join(Pedido.productos_pedidos).join(ProductoPedido.producto).filter(
            db.or_(
                Producto.nombre.ilike(f"%{param_producto}%"),
                Producto.id_producto.cast(db.String).ilike(f"%{param_producto}%"),
            )
        )

    if param_categoria:
        query = query.join(Pedido.productos_pedidos).join(ProductoPedido.producto).join(Producto.categoria).filter(
            Categoria.nombre.ilike(f"%{param_categoria}%"),
        )

    if param_marca:
        query = query.join(Pedido.productos_pedidos).join(ProductoPedido.producto).join(Producto.marca).filter(
            Marca.nombre.ilike(f"%{param_marca}%"),
        )
    
    if param_estado:
        query = query.filter(
            db.or_(
                Estado.estado.ilike(f"%{param_estado}%"),
                Estado.id_estado.cast(db.String).ilike(f"%{param_estado}%")
            )
        )

    pedidos_query = query.all()

    if not pedidos_query:
        return jsonify({
            "success": False, 
            "data": {"message": "No se encontraron pedidos."}
        }), 404

    pedidos = [
        {
            "id_pedido": pedido.id_pedido,
            "usuario": pedido.usuario.to_dict(),
            "fecha_pedido": pedido.fecha_pedido,
            "fecha_entrega": pedido.fecha_entrega,
            "valor_total": float(pedido.valor_total),
            "estado": pedido.estado.estado,
            "productos_pedidos": [
                {
                    "id_producto_pedido": pp.id_producto_pedido,
                    "producto": pp.producto.to_dict(),
                    "cantidad": pp.cantidad,
                }
                for pp in pedido.productos_pedidos
            ]
        }
        for pedido in pedidos_query
    ]

    if not pedidos:
        return jsonify({
            "success": False, 
            "data": {"message": "No se encontraron pedidos."}
        }), 404

    return jsonify({"success": True, "data": pedidos})

@pedidos_bp.route('/usuario/<int:id_usuario>', methods=['GET'])
def obtener_pedidos_usuario(id_usuario):
    
    Usuario.query.get_or_404(id_usuario, description="No se encontró el usuario.")
    
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    formato = "%Y-%m-%d"
    param_estado = request.args.get('estado')

    query = Pedido.query.options(
        joinedload(Pedido.productos_pedidos).joinedload(ProductoPedido.producto),
        joinedload(Pedido.usuario),
        joinedload(Pedido.estado),
    )

    try:
        if fecha_desde:
            fecha_desde = datetime.strptime(fecha_desde, formato).date()
        if fecha_hasta:
            fecha_hasta = datetime.strptime(fecha_hasta, formato).date()
    except ValueError:
        return jsonify({
            "success": False, 
            "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
        }), 400

    if fecha_desde:
        query = query.filter(Pedido.fecha_pedido >= fecha_desde)

    if fecha_hasta:
        query = query.filter(Pedido.fecha_pedido <= fecha_hasta)

    if param_estado:
        query = query.filter(
            db.or_(
                Estado.estado.ilike(f"%{param_estado}%"),
                Estado.id_estado.cast(db.String).ilike(f"%{param_estado}%")
            )
        )

    pedidos_query = query.filter(Pedido.id_usuario == id_usuario).all()

    if not pedidos_query:
        return jsonify({
            "success": False, 
            "data": {"message": "No se encontraron pedidos."}
        }), 404

    pedidos = [
        {
            "id_pedido": pedido.id_pedido,
            "usuario": pedido.usuario.to_dict(),
            "fecha_pedido": pedido.fecha_pedido,
            "fecha_entrega": pedido.fecha_entrega,
            "valor_total": float(pedido.valor_total),
            "estado": pedido.estado.estado,
            "productos_pedidos": [
                {
                    "id_producto_pedido": pp.id_producto_pedido,
                    "producto": pp.producto.to_dict(),
                    "cantidad": pp.cantidad,
                }
                for pp in pedido.productos_pedidos
            ]
        }
        for pedido in pedidos_query
    ]

    if not pedidos:
        return jsonify({
            "success": False, 
            "data": {"message": "No se encontraron pedidos."}
        }), 404

    return jsonify({"success": True, "data": pedidos})

@pedidos_bp.route('/categoria')
def obtener_pedidos_categoria():

    query = Pedido.query.options(
        joinedload(Pedido.productos_pedidos).joinedload(ProductoPedido.producto)
    ).join(Pedido.productos_pedidos).join(ProductoPedido.producto).join(Producto.categoria)

    try:
        pedidos = query.all()
        categorias_en_pedidos = defaultdict(list)

        for pedido in pedidos:
            for prod_pedido in pedido.productos_pedidos:
                categoria = prod_pedido.producto.categoria.nombre
                cantidad = prod_pedido.cantidad
                categorias_en_pedidos[categoria].append(cantidad)

        resultado = [{"categoria": k, "cantidad": sum(v)} for k, v in categorias_en_pedidos.items()]
        print(categorias_en_pedidos)
        
        return jsonify({"success": True, "data": resultado}), 200
    
    except ValueError:
        return jsonify({
            "success": False, 
            "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
        }), 400



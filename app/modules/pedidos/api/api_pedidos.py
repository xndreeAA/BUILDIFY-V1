from flask import Blueprint, jsonify, request, abort, current_app
from flask_login import login_required
from sqlalchemy.orm import joinedload
from sqlalchemy import func

from app.core.models.usuario import Usuario
from app.modules.pedidos.models import Pedido, ProductoPedido, Estado
from app.modules.productos.models import Producto, Categoria, Marca
from app.modules.pagos.models.factura import Factura
from datetime import datetime
from collections import defaultdict
from app import db

pedidos_bp = Blueprint('api_pedidos', __name__, url_prefix='/pedidos')

@pedidos_bp.route('/', methods=['GET'])
def obtener_pedidos():
    
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
        joinedload(Pedido.factura)
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
            ],
            "factura": pedido.factura.to_dict() if pedido.factura else {
                "error": f"No factura found for pedido {pedido.id_pedido}"
            }

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

@pedidos_bp.route('/historial-ventas-totales', methods=['GET'])
def obtener_pedidos_historial_ventas_totales():
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    fill = request.args.get('fill')

    formato = "%Y-%m-%d"

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

    query = db.session.query(
        func.extract('year', Pedido.fecha_pedido).label('year'),
        func.extract('month', Pedido.fecha_pedido).label('month'),
        func.sum(Pedido.valor_total).label('total')
    )

    if fecha_desde:
        query = query.filter(Pedido.fecha_pedido >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Pedido.fecha_pedido <= fecha_hasta)

    query = query.group_by('year', 'month').order_by('year', 'month')
    resultados = query.all()

    data = {}

    for year, month, total in resultados:
        year = int(year)
        month = int(month)

        if year not in data:
            data[year] = {
                "meses": { m: 0.0 for m in range(1, 13) } if fill == 'true' else {},
                "total_ventas": 0.0
            }

        data[year]["meses"][month] = float(total)
        data[year]["total_ventas"] += float(total)

    return jsonify({
        "success": True,
        "data": data
    })
from collections import defaultdict
from flask import jsonify

@pedidos_bp.route('/categoria')
def obtener_pedidos_categoria():
    query = Pedido.query.options(
        joinedload(Pedido.productos_pedidos).joinedload(ProductoPedido.producto)
    ).join(Pedido.productos_pedidos).join(ProductoPedido.producto).join(Producto.categoria)

    try:
        pedidos = query.all()
        
        categorias_en_pedidos = defaultdict(lambda: {"cantidad": 0, "ganancias": 0})

        for pedido in pedidos:
            for prod_pedido in pedido.productos_pedidos:
                categoria = prod_pedido.producto.categoria.nombre
                cantidad = prod_pedido.cantidad
                precio = prod_pedido.producto.precio
                total_producto = cantidad * precio

                categorias_en_pedidos[categoria]["cantidad"] += cantidad
                categorias_en_pedidos[categoria]["ganancias"] += total_producto

        resultado = [
            {
                "categoria": categoria,
                "cantidad": datos["cantidad"],
                "ganancias": round(datos["ganancias"], 2)
            }
            for categoria, datos in categorias_en_pedidos.items()
        ]

        return jsonify({"success": True, "data": resultado}), 200

    except ValueError:
        return jsonify({
            "success": False, 
            "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
        }), 400

    
def crear_query_pedidos(filtro=None, mas_vendido=True, fecha_desde=None, fecha_hasta=None):
    query = (
        db.session.query(
            Producto,
            func.sum(ProductoPedido.cantidad).label('unidades_vendidas')
        )
        .options(
            joinedload(Producto.categoria),
            joinedload(Producto.marca)
        )
        .join(ProductoPedido, Producto.id_producto == ProductoPedido.id_producto)
        .join(Pedido, Pedido.id_pedido == ProductoPedido.id_pedido)
        .join(Producto.categoria)
    )

    if filtro is not None:
        query = query.filter(filtro)

    query = query.group_by(Producto.id_producto)
    query = query.order_by(
        func.sum(ProductoPedido.cantidad).desc() if mas_vendido else func.sum(ProductoPedido.cantidad).asc()
    )

    formato = "%Y-%m-%d"

    if fecha_desde:
        fecha_desde = datetime.strptime(fecha_desde, formato).date()
        query = query.filter(Pedido.fecha_pedido >= fecha_desde)

    if fecha_hasta:
        fecha_hasta = datetime.strptime(fecha_hasta, formato).date()
        query = query.filter(Pedido.fecha_pedido <= fecha_hasta)

    resultado = query.first()


    if resultado:
        producto, unidades_vendidas = resultado
        return {
            'id_producto': producto.id_producto,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'categoria': producto.categoria.nombre,
            'marca': producto.marca.nombre,
            'unidades_vendidas': unidades_vendidas,
            'ganancias': unidades_vendidas * producto.precio
        }

    return None

 
@pedidos_bp.route('/mas-menos', methods=['GET'])
def obtener_pedidos_mas_menos():
       
    mas_vendido = request.args.get('mas_vendido')
    menos_vendido = request.args.get('menos_vendido')
    mas_vendido_categoria = request.args.get('mas_vendido_categoria')
    menos_vendido_categoria = request.args.get('menos_vendido_categoria')
    mas_vendido_marca = request.args.get('mas_vendido_marca')
    menos_vendido_marca = request.args.get('menos_vendido_marca')

    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')

    resultado = {
        'data': {},
        'success': False
    }

    if mas_vendido:

        try:

            mas_vendido_query = crear_query_pedidos(mas_vendido=True, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

            if mas_vendido_query:
                resultado['data']['mas_vendido'] = mas_vendido_query
                resultado['success'] = True

        except ValueError:
            return jsonify({
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }), 400
        
    if menos_vendido:
        try:

            menos_vendido_query = crear_query_pedidos(mas_vendido=False, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

            if menos_vendido_query:
                resultado['data']['menos_vendido'] = menos_vendido_query
                resultado['success'] = True

        except ValueError:
            return jsonify({
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }), 400
        

    if mas_vendido_categoria:
        try:
            
            nombre_categorias = db.session.query (
                Categoria.nombre
            ).all()

            categorias = [c[0] for c in nombre_categorias]

            if mas_vendido_categoria not in categorias:
                return jsonify({
                    "success": False, 
                    "data": {"message": "Categoria no encontrada."}
                }), 400

            filtro = Categoria.nombre == mas_vendido_categoria

            resultado_data = crear_query_pedidos(filtro=filtro, mas_vendido=True, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

            if resultado_data:
                resultado['data']['mas_vendido_categoria'] = resultado_data
                resultado['success'] = True
            else:
                return jsonify({
                    "success": False, 
                    "data": {"message": "Producto no encontrado en la búsqueda."}
                }), 400
            
        except ValueError as e:
            return jsonify({
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }), 400

    if menos_vendido_categoria:
        try:
            
            nombre_categorias = db.session.query (
                Categoria.nombre
            ).all()

            categorias = [c[0] for c in nombre_categorias]

            if menos_vendido_categoria not in categorias:
                return jsonify({
                    "success": False, 
                    "data": {"message": "Categoria no encontrada."}
                }), 400
            
            filtro = Categoria.nombre == menos_vendido_categoria

            resultado_data = crear_query_pedidos(filtro=filtro, mas_vendido=False, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

            if resultado_data:
                resultado['data']['menos_vendido_categoria'] = resultado_data
                resultado['success'] = True

            else:
                return jsonify({
                    "success": False, 
                    "data": {"message": "Producto no encontrado en la busqueda."}
                }), 400

        except ValueError as e:
            return jsonify({
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }), 400

    if menos_vendido_marca:

        try:
            nombre_marcas = db.session.query (
                Marca.nombre
            ).all()

            marcas = [m[0] for m in nombre_marcas]

            print (marcas)

            if menos_vendido_marca not in marcas:
                return jsonify({
                    "success": False, 
                    "data": {"message": "marca no encontrada."}
                }), 400
            
            filtro = Marca.nombre == menos_vendido_marca

            resultado_data = crear_query_pedidos(filtro=filtro, mas_vendido=False, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

            if resultado_data:
                resultado['data']['menos_vendido_marca'] = resultado_data
                resultado['success'] = True

            else:
                return jsonify({
                    "success": False, 
                    "data": {"message": "Producto no encontrado en la busqueda."}
                }), 400

        except ValueError as e:
            return jsonify({
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }), 400
    
    if mas_vendido_marca:

        try:
            nombre_marcas = db.session.query (
                Marca.nombre
            ).all()

            marcas = [m[0] for m in nombre_marcas]

            if mas_vendido_marca not in marcas:
                return jsonify({
                    "success": False, 
                    "data": {"message": "marca no encontrada."}
                }), 400
            
            filtro = Marca.nombre == mas_vendido_marca

            resultado_data = crear_query_pedidos(filtro=filtro, mas_vendido=True, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

            if resultado_data:
                resultado['data']['mas_vendido_marca'] = resultado_data
                resultado['success'] = True

            else:
                return jsonify({
                    "success": False, 
                    "data": {"message": "Producto no encontrado en la busqueda."}
                }), 400

        except ValueError as e:
            return jsonify({
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }), 400

    return jsonify(resultado)

@pedidos_bp.route('/get-pedido-by-session', methods=['GET'])
def get_pedido_by_session():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({
            "success": False,
            "error": "Falta el parámetro session_id"
        }), 400

    pedido = (
        Pedido.query
        .options(
            joinedload(Pedido.factura),
            joinedload(Pedido.usuario)  
        )
        .filter_by(stripe_session_id=session_id)
        .first()
    )

    if not pedido:
        return jsonify({
            "success": False,
            "error": "Pedido no encontrado"
        }), 404

    factura_data = pedido.factura.to_dict() if pedido.factura else None

    return jsonify({
        "success": True,
        "data" : {            
            "id_pedido": pedido.id_pedido,
            "id_usuario": pedido.id_usuario,
            "email": pedido.usuario.email,
            "fecha_pedido": pedido.fecha_pedido.isoformat() if pedido.fecha_pedido else None,
            "valor_total": float(pedido.valor_total),
            "factura": factura_data
        }
    })
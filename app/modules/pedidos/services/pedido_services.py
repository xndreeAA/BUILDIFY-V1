from sqlalchemy.orm import joinedload
from sqlalchemy import func
from collections import defaultdict
from datetime import datetime
from app.modules.pedidos.models import Pedido, ProductoPedido, Estado
from app.modules.productos.models import Producto, Categoria, Marca
from app import db

class PedidoServices:

    @staticmethod
    def obtener_pedidos(filters):
            
        query = Pedido.query.options(
            joinedload(Pedido.productos_pedidos).joinedload(ProductoPedido.producto),
            joinedload(Pedido.usuario),
            joinedload(Pedido.estado),
            joinedload(Pedido.factura)
        )

        formato = "%Y-%m-%d"
        fecha_desde = filters.get('fecha_desde')
        fecha_hasta = filters.get('fecha_hasta')
        param_producto = filters.get('producto')
        param_categoria = filters.get('categoria')
        param_marca = filters.get('marca')
        param_estado = filters.get('estado')

        try:
            if fecha_desde:
                fecha_desde = datetime.strptime(fecha_desde, formato).date()
            if fecha_hasta:
                fecha_hasta = datetime.strptime(fecha_hasta, formato).date()
        except ValueError:
            return {
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }, 400

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
            return {
                "success": False, 
                "data": {"message": "No se encontraron pedidos."}
            }, 404

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
            return {
                "success": False, 
                "data": {"message": "No se encontraron pedidos."}
            }, 404

        return {"success": True, "data": pedidos}, 200

    @staticmethod
    def obtener_pedidos_usuario(id_usuario, filters):
            
        query = Pedido.query.options(
            joinedload(Pedido.productos_pedidos).joinedload(ProductoPedido.producto),
            joinedload(Pedido.usuario),
            joinedload(Pedido.estado),
            joinedload(Pedido.factura)
        )

        formato = "%Y-%m-%d"
        fecha_desde = filters.get('fecha_desde')
        fecha_hasta = filters.get('fecha_hasta')
        param_estado = filters.get('estado')

        try:
            if fecha_desde:
                fecha_desde = datetime.strptime(fecha_desde, formato).date()
            if fecha_hasta:
                fecha_hasta = datetime.strptime(fecha_hasta, formato).date()
        except ValueError:
            return {
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }, 400

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
            return {
                "success": False, 
                "data": {"message": "No se encontraron pedidos."}
            }, 404

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

        return {"success": True, "data": pedidos}, 200

    @staticmethod
    def obtener_historial_ventas_totales(filters):
        
        fecha_desde = filters.get('fecha_desde')
        fecha_hasta = filters.get('fecha_hasta')
        fill = filters.get('fill')

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

        return {
            "success": True,
            "data": data
        }, 200
    
    @staticmethod
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

            return {"success": True, "data": resultado}, 200

        except ValueError:
            return {
                "success": False, 
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }, 400

    @staticmethod
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
   
    @staticmethod
    def obtener_pedidos_mas_menos(filters):
        mas_vendido = filters.get('mas_vendido')
        menos_vendido = filters.get('menos_vendido')
        mas_vendido_categoria = filters.get('mas_vendido_categoria')
        menos_vendido_categoria = filters.get('menos_vendido_categoria')
        mas_vendido_marca = filters.get('mas_vendido_marca')
        menos_vendido_marca = filters.get('menos_vendido_marca')
        fecha_desde = filters.get('fecha_desde')
        fecha_hasta = filters.get('fecha_hasta')

        resultado = {"data": {}, "success": False}

        try:
            if mas_vendido:
                q = PedidoServices.crear_query_pedidos(mas_vendido=True, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
                if q: 
                    resultado["data"]["mas_vendido"] = q
                    resultado["success"] = True

            if menos_vendido:
                q = PedidoServices.crear_query_pedidos(mas_vendido=False, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
                if q: 
                    resultado["data"]["menos_vendido"] = q
                    resultado["success"] = True

            if mas_vendido_categoria:
                ok, res = PedidoServices._obtener_por_modelo(Categoria, "Categoria", mas_vendido_categoria, True, fecha_desde, fecha_hasta)
                if ok: 
                    resultado["data"]["mas_vendido_categoria"] = res
                    resultado["success"] = True
                else:
                    return {"success": False, "data": res}, 400

            if menos_vendido_categoria:
                ok, res = PedidoServices._obtener_por_modelo(Categoria, "Categoria", menos_vendido_categoria, False, fecha_desde, fecha_hasta)
                if ok: 
                    resultado["data"]["menos_vendido_categoria"] = res
                    resultado["success"] = True
                else:
                    return {"success": False, "data": res}, 400

            if mas_vendido_marca:
                ok, res = PedidoServices._obtener_por_modelo(Marca, "Marca", mas_vendido_marca, True, fecha_desde, fecha_hasta)
                if ok: 
                    resultado["data"]["mas_vendido_marca"] = res
                    resultado["success"] = True
                else:
                    return {"success": False, "data": res}, 400

            if menos_vendido_marca:
                ok, res = PedidoServices._obtener_por_modelo(Marca, "Marca", menos_vendido_marca, False, fecha_desde, fecha_hasta)
                if ok: 
                    resultado["data"]["menos_vendido_marca"] = res
                    resultado["success"] = True
                else:
                    return {"success": False, "data": res}, 400

            return resultado, 200

        except ValueError:
            return {"success": False, "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}}, 400

    @staticmethod
    def _obtener_por_modelo(modelo, nombre_campo, valor, mas_vendido, fecha_desde, fecha_hasta):
        nombres = [n[0] for n in db.session.query(modelo.nombre).all()]
        if valor not in nombres:
            return False, {"message": f"{nombre_campo} no encontrada."}

        filtro = modelo.nombre == valor
        resultado_data = PedidoServices.crear_query_pedidos(
            filtro=filtro, mas_vendido=mas_vendido,
            fecha_desde=fecha_desde, fecha_hasta=fecha_hasta
        )

        if resultado_data:
            return True, resultado_data
        return False, {"message": "Producto no encontrado en la búsqueda."}

    @staticmethod
    def obtener_pedido_by_session(session_id):
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
            return {
                "success": False,
                "error": "Pedido no encontrado"
            }, 404

        factura_data = pedido.factura.to_dict() if pedido.factura else None

        return {
            "success": True,
            "data" : {            
                "id_pedido": pedido.id_pedido,
                "id_usuario": pedido.id_usuario,
                "email": pedido.usuario.email,
                "fecha_pedido": pedido.fecha_pedido.isoformat() if pedido.fecha_pedido else None,
                "valor_total": float(pedido.valor_total),
                "factura": factura_data
            }
        }, 200

        
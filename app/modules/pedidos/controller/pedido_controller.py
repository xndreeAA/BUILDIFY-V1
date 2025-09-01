from flask import request, jsonify
import datetime
from app.core.models.usuario import Usuario
from app.modules.pedidos.services.pedido_services import PedidoServices

class PedidoController:
    @staticmethod
    def obtener_pedidos(*args, **kwargs):
        
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        param_producto = request.args.get('producto')
        param_categoria = request.args.get('categoria')
        param_marca = request.args.get('marca')
        param_estado = request.args.get('estado')

        filters = {}

        if fecha_desde:
            filters['fecha_desde'] = fecha_desde
        if fecha_hasta:
            filters['fecha_hasta'] = fecha_hasta
        if param_producto:
            filters['producto'] = param_producto
        if param_categoria:
            filters['categoria'] = param_categoria
        if param_marca:
            filters['marca'] = param_marca
        if param_estado:
            filters['estado'] = param_estado

        data, status = PedidoServices.obtener_pedidos(filters)

        return jsonify(data), status

    @staticmethod
    def obtener_pedidos_usuario(id_usuario, *args, **kwargs):

        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return jsonify({"success": False, "error": "No se encontró el usuario."}), 404

        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        param_estado = request.args.get('estado')

        filters = {}

        if fecha_desde:
            filters['fecha_desde'] = fecha_desde
        if fecha_hasta:
            filters['fecha_hasta'] = fecha_hasta
        if param_estado:
            filters['estado'] = param_estado


        data, status = PedidoServices.obtener_pedidos_usuario(usuario.id_usuario, filters)

        return jsonify(data), status
    
    @staticmethod
    def obtener_historial_ventas_totales(*args, **kwargs):

        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        fill = request.args.get('fill')
        formato = "%Y-%m-%d"

        filters = {}
        
        try:
            if fecha_desde:
                fecha_desde = datetime.strptime(fecha_desde, formato).date()
                filters['fecha_desde'] = fecha_desde
            if fecha_hasta:
                fecha_hasta = datetime.strptime(fecha_hasta, formato).date()
                filters['fecha_hasta'] = fecha_hasta
            if fill:
                filters['fill'] = fill
        except ValueError:
            return jsonify({
                "success": False,
                "data": {"message": "Formato de fecha incorrecto. Utiliza YYYY-MM-DD."}
            }), 400

        data, status = PedidoServices.obtener_historial_ventas_totales(filters)

        return jsonify(data), status
    
    @staticmethod
    def obtener_pedidos_categoria(*args, **kwargs):

        data, status = PedidoServices.obtener_pedidos_categoria()

        return jsonify(data), status
    
    @staticmethod
    def obtener_pedidos_mas_menos(*args, **kwargs):

        mas_vendido = request.args.get('mas_vendido')
        menos_vendido = request.args.get('menos_vendido')
        mas_vendido_categoria = request.args.get('mas_vendido_categoria')
        menos_vendido_categoria = request.args.get('menos_vendido_categoria')
        mas_vendido_marca = request.args.get('mas_vendido_marca')
        menos_vendido_marca = request.args.get('menos_vendido_marca')

        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')

        filters = {}

        if mas_vendido:
            filters['mas_vendido'] = mas_vendido
        if menos_vendido:
            filters['menos_vendido'] = menos_vendido
        if mas_vendido_categoria:
            filters['mas_vendido_categoria'] = mas_vendido_categoria
        if menos_vendido_categoria:
            filters['menos_vendido_categoria'] = menos_vendido_categoria
        if mas_vendido_marca:
            filters['mas_vendido_marca'] = mas_vendido_marca
        if menos_vendido_marca:
            filters['menos_vendido_marca'] = menos_vendido_marca
        if fecha_desde:
            filters['fecha_desde'] = fecha_desde
        if fecha_hasta:
            filters['fecha_hasta'] = fecha_hasta

        data, status = PedidoServices.obtener_pedidos_mas_menos(filters)

        return jsonify(data), status
    
    @staticmethod
    def get_pedido_by_session (*args, **kwargs):
        session_id = request.args.get('session_id')
        if not session_id:
            return jsonify({
                "success": False,
                "error": "Falta el parámetro session_id"
            }), 400

        data, status = PedidoServices.obtener_pedido_by_session(session_id)

        return jsonify(data), status
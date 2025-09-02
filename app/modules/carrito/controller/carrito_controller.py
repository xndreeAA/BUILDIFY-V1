from flask import jsonify, request, abort
from flask_login import  current_user
from app.core.models.usuario import Usuario
from app.modules.carrito.services.carrito_services import CarritoService

class CarritoController:
    @staticmethod
    def obtener_carrito(*args, **kwargs):
        id_usuario = current_user.get_id() if current_user.is_authenticated else None
        if not id_usuario:
            abort(401, description="No autenticado.")

        Usuario.query.get_or_404(id_usuario, description="Usuario no encontrado.")

        carrito, items = CarritoService.obtener_carrito(id_usuario)

        return jsonify({
            "success": True,
            "carrito": {
                "id_carrito": carrito.id_carrito,
                "items": [item.to_dict() for item in items],
                "total": float(sum(item.producto.precio * item.cantidad for item in items))
            }
        })

    @staticmethod
    def anadir_producto_carrito(*args, **kwargs):
        
        payload = request.get_json(silent=True)
        
        id_usuario = current_user.get_id() if current_user.is_authenticated else None
        if not id_usuario:
            abort(401, description="No autenticado.")

        if not payload:
            abort(400, description="Request body debe ser JSON válido")

        campos_requeridos = ["id_producto", "cantidad"]

        for campo in campos_requeridos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        id_producto = payload["id_producto"]
        cantidad = payload["cantidad"]
        
        data, status = CarritoService.anadir_producto_carrito(id_usuario, id_producto, cantidad)

        return jsonify(data), status
    
    @staticmethod
    def eliminar_producto_carrito(*args, **kwargs):

        id_usuario = current_user.get_id() if current_user.is_authenticated else None
        if not id_usuario:
            abort(401, description="No autenticado.")

        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido")

        campos_requeridos = ["id_producto"]
        for campo in campos_requeridos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        id_producto = payload["id_producto"]

        data, status = CarritoService.eliminar_producto_carrito(id_usuario, id_producto)

        return jsonify(data), status

    @staticmethod
    def modificar_cantidad_producto_carrito(*args, **kwargs):

        id_usuario = current_user.get_id() if current_user.is_authenticated else None

        if not id_usuario:
            abort(401, description="No autenticado.")

        payload = request.get_json(silent=True)

        if not payload:
            abort(400, description="Request body debe ser JSON válido")

        campos_requeridos = ["id_producto", "cantidad"]
        for campo in campos_requeridos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        id_producto = payload["id_producto"]
        cantidad = payload["cantidad"]

        data, status = CarritoService.modificar_cantidad_producto_carrito(id_usuario, id_producto, cantidad)

        return jsonify(data), status
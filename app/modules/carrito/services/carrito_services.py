from flask import abort, jsonify
from sqlalchemy.orm import joinedload
from app.modules.carrito.models.carrito import Carrito
from app.modules.carrito.models.item_carrito import ItemCarrito
from app.modules.productos.models.producto import Producto
from app import db

class CarritoService:
    
    @staticmethod
    def obtener_carrito(id_usuario):
        carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
        if not carrito:
            carrito = Carrito(id_usuario=id_usuario)
            db.session.add(carrito)
            db.session.commit()

        items = ItemCarrito.query.options(
            joinedload(ItemCarrito.producto).joinedload(Producto.imagenes),
            joinedload(ItemCarrito.producto).joinedload(Producto.categoria),
            joinedload(ItemCarrito.producto).joinedload(Producto.marca)
        ).filter_by(id_carrito=carrito.id_carrito).all()
    
        return carrito, items
    
    @staticmethod
    def anadir_producto_carrito(id_usuario, id_producto, cantidad):

        carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
        if not carrito:
            carrito = Carrito(id_usuario=id_usuario)
            db.session.add(carrito)
            db.session.commit()

        producto = Producto.query.get(id_producto)

        if not producto:
            return {
                "success": False,
                "error": "Producto no encontrado."
            }, 404

        if not isinstance(cantidad, int) or cantidad <= 0:
            return {
                "success": False,
                "error": "La cantidad debe ser un número entero positivo."
            }, 400
        elif cantidad > producto.stock:
            return {
                "success": False,
                "error": "La cantidad excede el stock disponible."
            }, 400

        item_existente = ItemCarrito.query.filter_by(
            id_carrito=carrito.id_carrito,
            id_producto=producto.id_producto
        ).first()

        nuevo_item = None 

        if not item_existente:
            nuevo_item = ItemCarrito(
                id_carrito=carrito.id_carrito,
                id_producto=producto.id_producto,
                cantidad=cantidad
            )
            db.session.add(nuevo_item)
            db.session.commit()
            return {"success": True, "item": nuevo_item.to_dict()}, 201
        
        return {"success": False, "error": "El producto ya estaba en el carrito."}, 409
    
    @staticmethod
    def eliminar_producto_carrito(id_usuario, id_producto):
       
        carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()

        if not carrito:
            return {
                "success": False,
                "error": "El carrito no existe."
            }, 404

        producto = Producto.query.get(id_producto)

        if not producto:
            return jsonify({
                "success": False,
                "error": "Producto no encontrado."
            }), 404

        item_carrito = ItemCarrito.query.filter_by(
            id_carrito=carrito.id_carrito,
            id_producto=producto.id_producto
        ).first()

        if not item_carrito:
            return jsonify({
                "success": False,
                "error": "El producto no estaba en el carrito."
            }), 404

        db.session.delete(item_carrito)
        db.session.commit()

        return {
            "success": True,
            "item": item_carrito.to_dict()
        }, 200
        
    @staticmethod
    def modificar_cantidad_producto_carrito(id_usuario, id_producto, cantidad):        
        carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
        if not carrito:
            return {
                "success": False,
                "error": "El carrito no existe."
            }, 404

        producto = Producto.query.get(id_producto)

        if not producto:
            return {
                "success": False,
                "error": "Producto no encontrado."
            }, 404

        item_carrito = ItemCarrito.query.filter_by(
            id_carrito=carrito.id_carrito,
            id_producto=producto.id_producto
        ).first()

        if not item_carrito:
            return {
                "success": False,
                "error": "El producto no estaba en el carrito."
            }, 404

        if not isinstance(cantidad, int) or cantidad <= 0:  
            return {
                "success": False,
                "error": "La cantidad debe ser un número entero positivo."
            }, 400
        elif cantidad > producto.stock:
            abort(400, description="La cantidad excede el stock disponible.")
        if cantidad == 0:
            db.session.delete(item_carrito)
            db.session.commit()
            return {
                "success": True,
                "removed": True
            }, 200
        
        item_carrito.cantidad = cantidad
        db.session.commit()

        return {
            "success": True,
            "item": item_carrito.to_dict()
        }, 200

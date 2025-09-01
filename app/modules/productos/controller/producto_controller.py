from flask import request, jsonify, abort
from app.modules.productos.services.producto_services import ProductoServices


class ProductoController:
    @staticmethod 
    def obtener_productos(*args, **kwargs):

        busqueda = request.args.get('busqueda')
        categoria_nombre = request.args.get('categoria')
        marca_nombre = request.args.get('marca')

        if categoria_nombre:
            categoria_nombre = categoria_nombre.lower()
        if marca_nombre:
            marca_nombre = marca_nombre.lower()

        data, status = ProductoServices.obtener_productos(busqueda, categoria_nombre, marca_nombre)

        return jsonify(data), status

    @staticmethod 
    def crear_producto(*args, **kwargs):
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos_requeridos = ["nombre", "precio", "stock", "id_marca", "id_categoria", "detalles"]
        for campo in campos_requeridos:
            if campo not in payload:
                abort(400, description=f"Falta el campo obligatorio: {campo}")

        data, status = ProductoServices.crear_producto(payload)

        return jsonify(data), status
    
    @staticmethod
    def traer_un_producto(id_producto, *args, **kwargs):

        data, status = ProductoServices.traer_un_producto(id_producto)

        return jsonify(data), status
    
    @staticmethod
    def eliminar_producto(id_producto, *args, **kwargs):
        print(id_producto)
        data, status = ProductoServices.eliminar_producto(id_producto)

        return jsonify(data), status
    
    @staticmethod
    def modificar_producto(id_producto, *args, **kwargs):

        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos = ["nombre", "precio", "stock", "id_categoria", "id_marca"]
        for campo in campos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        data, status = ProductoServices.modificar_producto(id_producto, payload)

        return jsonify(data), status
    
    @staticmethod
    def subir_imagenes_producto(id_producto, *args, **kwargs):

        imagenes = request.files.getlist('imagenes')
        id_producto = request.form.get('id_producto')
        categoria = request.form.get('categoria')
        principales = request.form.getlist('es_principal')

        if not imagenes or not id_producto or not categoria:
            abort(400, description="Faltan datos requeridos.")

        data, status = ProductoServices.subir_imagenes_producto(
            id_producto=id_producto,
            imagenes=imagenes,
            categoria=categoria,
            principales=principales
        )

        return jsonify(data), status
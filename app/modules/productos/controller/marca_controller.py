from flask import request, jsonify, abort
from app.modules.productos.services.marca_services import MarcaService

class MarcasController:

    @staticmethod
    def handle_marcas():
        if request.method == 'GET':
            marcas = MarcaService.get_all_marcas()
            return jsonify({"success": True, "data": marcas})

        elif request.method == 'POST':
            payload = request.get_json(silent=True)
            if not payload or not payload.get("nombre"):
                abort(400, description="El campo 'nombre' es obligatorio.")
            
            nueva_marca = MarcaService.create_marca(payload["nombre"])
            return jsonify({"success": True, "data": nueva_marca})

    @staticmethod
    def handle_marca_by_id(id_marca):
        if request.method == 'GET':
            marca = MarcaService.get_marca_by_id(id_marca)
            return jsonify({"success": True, "data": marca})

        elif request.method == 'PUT':
            payload = request.get_json(silent=True)
            if not payload:
                abort(400, description="Request body debe ser JSON válido.")

            marca_actualizada = MarcaService.update_marca(id_marca, payload.get("nombre"))
            return jsonify({"success": True, "data": marca_actualizada})

        elif request.method == 'DELETE':
            MarcaService.delete_marca(id_marca)
            return jsonify({"success": True})

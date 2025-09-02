from flask import request, jsonify, abort
from app.modules.productos.services.categoria_services import CategoriaService

class CategoriasController:

    @staticmethod
    def handle_categorias():
        if request.method == 'GET':
            categorias = CategoriaService.get_all_categorias()
            return jsonify({"success": True, "data": categorias})

        elif request.method == 'POST':
            payload = request.get_json(silent=True)
            if not payload or not payload.get("nombre"):
                abort(400, description="El campo 'nombre' es obligatorio.")
            
            nueva_categoria = CategoriaService.create_categoria(payload["nombre"])
            return jsonify({"success": True, "data": nueva_categoria})

        else:
            abort(400, description="Método no permitido.")

    @staticmethod
    def handle_categoria_by_id(id_categoria):
        if request.method == 'GET':
            categoria = CategoriaService.get_categoria_by_id(id_categoria)
            return jsonify({"success": True, "data": categoria})

        elif request.method == 'PUT':
            payload = request.get_json(silent=True)
            if not payload:
                abort(400, description="Request body debe ser JSON válido.")

            categoria_actualizada = CategoriaService.update_categoria(id_categoria, payload.get("nombre"))
            return jsonify({"success": True, "data": categoria_actualizada})

        elif request.method == 'DELETE':
            CategoriaService.delete_categoria(id_categoria)
            return jsonify({"success": True})

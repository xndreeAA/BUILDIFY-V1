"""
Controlador que gestiona el CRUD de los items del carrusel.
Incluye endpoints para listar, crear, actualizar, eliminar y subir imágenes
(asociadas o no a un item). La lógica de negocio y acceso a datos se delega
a `CarruselService`.
"""

from flask import request, jsonify
from app.modules.landing.services.carrusel_services import CarruselService

# Extensiones permitidas de imágenes
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename: str) -> bool:

    #Verifica si el archivo tiene una extensión válida. 
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class CarruselController:
    # Controlador para los endpoints del carrusel.
    # ---------- CRUD BÁSICO ----------

    @staticmethod
    def obtener_items():
        # Retorna todos los items del carrusel.
        items = CarruselService.obtener_todos()
        return jsonify({"success": True, "data": [i.to_dict() for i in items]}), 200

    @staticmethod
    def crear_item():
        """
        Crea un nuevo item de carrusel.
        - Acepta datos en JSON o multipart/form-data.
        - Si se adjunta imagen, se sube automáticamente y se asocia al item.
        """
        data = request.get_json() if request.is_json else request.form.to_dict()

        # Validación mínima
        if not data or not data.get("titulo"):
            return jsonify({"success": False, "message": "El campo 'titulo' es obligatorio."}), 400

        # Crear item sin imagen
        item = CarruselService.crear(data)

        # Si viene imagen, subir y asociar
        if "imagen" in request.files and request.files["imagen"].filename:
            upload_res = CarruselService.guardar_imagen(request.files["imagen"], id_carrusel=item.id_carrusel)

            # Normalización de respuestas de servicio
            if isinstance(upload_res, tuple):  # (body, status)
                body, status = upload_res
                if not body.get("success"):
                    return jsonify(body), status
            elif isinstance(upload_res, dict) and not upload_res.get("success", True):
                return jsonify(upload_res), 500

            # Recargar item con la imagen
            item = CarruselService.obtener_por_id(item.id_carrusel)

        return jsonify({"success": True, "data": item.to_dict()}), 201

    @staticmethod
    def traer_un_item(id_carrusel: int):
        # Retorna un item de carrusel por su ID.
        item = CarruselService.obtener_por_id(id_carrusel)
        if not item:
            return jsonify({"success": False, "message": "No encontrado"}), 404
        return jsonify({"success": True, "data": item.to_dict()}), 200

    @staticmethod
    def modificar_item(id_carrusel: int):
        #Actualiza un item del carrusel.
        data = request.get_json() if request.is_json else request.form.to_dict()
        item = CarruselService.actualizar(id_carrusel, data)

        if not item:
            return jsonify({"success": False, "message": "No actualizado"}), 400

        # Si viene imagen nueva, actualizarla
        if "imagen" in request.files and request.files["imagen"].filename:
            upload_res = CarruselService.guardar_imagen(request.files["imagen"], id_carrusel=item.id_carrusel)

            if isinstance(upload_res, tuple):
                body, status = upload_res
                if not body.get("success"):
                    return jsonify(body), status
            elif isinstance(upload_res, dict) and not upload_res.get("success", True):
                return jsonify(upload_res), 500

            # Recargar item con datos actualizados
            item = CarruselService.obtener_por_id(item.id_carrusel)

        return jsonify({"success": True, "data": item.to_dict()}), 200

    @staticmethod
    def eliminar_item(id_carrusel: int):
        # Elimina un item del carrusel por su ID.
        ok = CarruselService.eliminar(id_carrusel)
        if not ok:
            return jsonify({"success": False, "message": "No eliminado"}), 400
        return jsonify({"success": True, "message": "Eliminado"}), 200

    # ---------- ENDPOINT ESPECIAL ----------

    @staticmethod
    def subir_imagen():
        """
        Sube una imagen a Cloudinary en la carpeta `buildify/carrusel`.
        Puede usarse de forma independiente para obtener la URL de la imagen,
        sin asociarla a un item todavía.
        """
        if "imagen" not in request.files:
            return jsonify({"success": False, "message": "No hay archivo 'imagen'"}), 400

        file = request.files["imagen"]

        if file.filename == "":
            return jsonify({"success": False, "message": "Archivo sin nombre"}), 400

        if file and allowed_file(file.filename):
            res = CarruselService.guardar_imagen(file, id_carrusel=None)

            if isinstance(res, tuple):
                body, status = res
                return jsonify(body), status
            return jsonify(res), 201

        return jsonify({"success": False, "message": "Extensión no permitida"}), 400

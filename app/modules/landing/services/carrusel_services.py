"""
Encapsula la lógica de negocio y persistencia del carrusel.
Incluye operaciones CRUD y manejo de imágenes con Cloudinary.
"""

import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename
from flask import current_app
from app import db
from app.modules.landing.models.carrusel import Carrusel

# Extensiones de imagen permitidas
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


class CarruselService:
    # Servicio que provee operaciones para gestionar items del carrusel.

    @staticmethod
    def allowed_file(filename: str) -> bool:
        # Verifica si un archivo tiene una extensión válida.
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    # ---------- Operaciones CRUD ----------

    @staticmethod
    def obtener_todos():
        # Obtiene todos los items del carrusel en orden descendente por ID.
        return Carrusel.query.order_by(Carrusel.id_carrusel.desc()).all()

    @staticmethod
    def crear(data: dict) -> Carrusel:
        # Crea un nuevo item de carrusel.
        item = Carrusel(
            titulo=data.get("titulo", "")[:150],
            descripcion=data.get("descripcion", "")
        )
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def obtener_por_id(id_carrusel: int):
        # Retorna un item por ID.
        return Carrusel.query.get(id_carrusel)

    @staticmethod
    def actualizar(id_carrusel: int, data: dict):
        # Actualiza título y descripción de un item.
        item = Carrusel.query.get(id_carrusel)
        if not item:
            return None

        item.titulo = data.get("titulo", item.titulo)
        item.descripcion = data.get("descripcion", item.descripcion)
        db.session.commit()
        return item

    @staticmethod
    def eliminar(id_carrusel: int) -> bool:
        """
        Elimina un item del carrusel.
        También borra la imagen asociada de Cloudinary si existe.
        """
        item = Carrusel.query.get(id_carrusel)
        if not item:
            return False

        if item.public_id:
            try:
                cloudinary.config(
                    cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
                    api_key=current_app.config.get("CLOUDINARY_API_KEY"),
                    api_secret=current_app.config.get("CLOUDINARY_API_SECRET")
                )
                cloudinary.uploader.destroy(
                    item.public_id,
                    invalidate=True,
                    resource_type="image"
                )
            except Exception as e:
                current_app.logger.error(f"Error borrando imagen Cloudinary: {e}")

        db.session.delete(item)
        db.session.commit()
        return True

    # ---------- Manejo de imágenes ----------

    @staticmethod
    def guardar_imagen(file_storage, id_carrusel=None):
        """
        Sube una imagen a Cloudinary en la carpeta `buildify/carrusel`.
        Si se pasa un `id_carrusel`, la imagen se asocia a ese registro.
        """
        if file_storage is None or not CarruselService.allowed_file(file_storage.filename):
            return {"success": False, "message": "Archivo no válido."}, 400

        filename = secure_filename(file_storage.filename)

        try:
            # Configuración dinámica de Cloudinary
            cloudinary.config(
                cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
                api_key=current_app.config.get("CLOUDINARY_API_KEY"),
                api_secret=current_app.config.get("CLOUDINARY_API_SECRET")
            )

            # Subir archivo a carpeta específica
            upload_result = cloudinary.uploader.upload(
                file_storage,
                folder="buildify/carrusel",
                use_filename=True,
                unique_filename=True  # asegura nombres únicos
            )

        except Exception as e:
            current_app.logger.error(f"Error al subir imagen a Cloudinary: {e}")
            return {"success": False, "message": "Error al subir imagen a Cloudinary."}, 500

        url = upload_result.get("secure_url")
        public_id = upload_result.get("public_id")

        if not url or not public_id:
            return {"success": False, "message": "No se pudo obtener URL/public_id."}, 500

        # Asociar imagen a un item existente
        if id_carrusel:
            item = Carrusel.query.get(id_carrusel)
            if item:
                # Si ya existía una imagen previa, borrarla
                if item.public_id and item.public_id != public_id:
                    try:
                        cloudinary.uploader.destroy(item.public_id, invalidate=True, resource_type="image")
                    except Exception:
                        pass

                item.url_imagen = url
                item.public_id = public_id
                db.session.commit()
                return {"success": True, "data": item.to_dict()}, 200

        #Respuesta si no se asocia a un item todavía
        return {
            "success": True,
            "url": url,
            "public_id": public_id,
            "filename": filename
        }, 201

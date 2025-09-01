from flask import current_app, abort
from sqlalchemy import or_
from app import db
import traceback
import os
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename
from cloudinary import config, api
from app.modules.productos.models import (
    Producto, Categoria, Marca, ImagenesProducto,
    DetalleChasis, DetalleFuentePoder, DetalleMemoriaRAM,
    DetallePlacaBase, DetalleProcesador, DetalleRefrigeracion,
    DetalleTarjetaGrafica
)

class ProductoServices:
    MAPA_DETALLES = {
        1: DetalleProcesador,
        2: DetalleMemoriaRAM,
        3: DetalleTarjetaGrafica,
        4: DetalleChasis,
        5: DetalleRefrigeracion,
        6: DetalleFuentePoder,
        7: DetallePlacaBase,
    }

    @staticmethod
    def obtener_productos(busqueda, categoria_nombre, marca_nombre):
        
        query = Producto.query.options(
            db.joinedload(Producto.categoria),
            db.joinedload(Producto.marca),
            db.joinedload(Producto.imagenes)
        )
        if busqueda:
            query = query.join(Producto.categoria).filter(
                or_(
                    Producto.nombre.ilike(f"%{busqueda}%"),
                    Categoria.nombre.ilike(f"%{busqueda}%"),
                    Marca.nombre.ilike(f"%{busqueda}%")
                )
            )
        if marca_nombre:
            query = query.join(Producto.marca).filter(Marca.nombre == marca_nombre)
        if categoria_nombre:
            query = query.join(Producto.categoria).filter(Categoria.nombre == categoria_nombre)

        productos = query.all()
        productos_data = [producto.to_dict() for producto in productos]

        return { 
            "success": True, 
            "data": productos_data 
        }, 200
    
    @staticmethod
    def crear_producto(payload):
        nuevo_producto = Producto(
            nombre=payload["nombre"],
            precio=payload["precio"],
            stock=payload["stock"],
            id_marca=payload["id_marca"],
            id_categoria=payload["id_categoria"]
        )

        db.session.add(nuevo_producto)
        db.session.flush()

        modelo_detalle = ProductoServices.MAPA_DETALLES.get(payload["id_categoria"])
        if modelo_detalle:
            detalles_payload = payload["detalles"]
            detalle = modelo_detalle(id_producto=nuevo_producto.id_producto, **detalles_payload)
            db.session.add(detalle)

        for imagen in payload.get("imagenes", []):
            
            if "ruta" not in imagen or "es_principal" not in imagen:
                return { 
                    "success": False, 
                    "message": "400, description=Cada imagen debe tener 'ruta' y 'es_principal'" 
                }, 400
            
            nueva_imagen = ImagenesProducto(
                id_producto=nuevo_producto.id_producto,
                nombre_archivo=imagen["ruta"],
                es_principal=imagen["es_principal"]
            )
            db.session.add(nueva_imagen)

        db.session.commit()

        return { 
            "success": True, 
            "data": {
                "id_producto": nuevo_producto.id_producto 
            }
        }, 201
    
    @staticmethod
    def traer_un_producto(id_producto):
        print(id_producto)
        producto = Producto.query.options(
            db.joinedload(Producto.categoria),
            db.joinedload(Producto.marca),
            db.joinedload(Producto.imagenes)
        ).filter_by(id_producto=id_producto).first()

        if not producto:
            return {
                "success": False,
                "error": "Producto no encontrado"
            }, 404
        
        return { 
            "success": True, 
            "data": producto.to_dict() 
        }, 200

    @staticmethod
    def eliminar_producto(id_producto):
        try:
            producto = Producto.query.get(id_producto)

            if not producto:
                return {
                    "success": False,
                    "error": "Producto no encontrado"
                }, 404

            config(
                cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
                api_key=current_app.config.get("CLOUDINARY_API_KEY"),
                api_secret=current_app.config.get("CLOUDINARY_API_SECRET")
            )

            carpeta = f"buildify/productos/{producto.categoria.nombre}/producto_{id_producto}"

            try:
                api.delete_resources_by_prefix(carpeta)
                api.delete_folder(carpeta)

            except Exception as ce:
                print(f"Error eliminando en Cloudinary: {ce} — Continuando con eliminación en DB")

            db.session.delete(producto)
            db.session.commit()
            print("Producto eliminado correctamente")

            return {"success": True}, 204

        except Exception as e:
            db.session.rollback()
            print("ERROR AL ELIMINAR PRODUCTO:")
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "tipo": type(e).__name__
            }, 400

    @staticmethod
    def modificar_producto(id_producto, payload):

        producto = Producto.query.get(id_producto)

        if not producto:
            return {
                "success": False,
                "error": "Producto no encontrado"
            }, 404

        producto.nombre = payload["nombre"]
        producto.precio = payload["precio"]
        producto.stock = payload["stock"]
        producto.id_categoria = payload["id_categoria"]
        producto.id_marca = payload["id_marca"]

        db.session.commit()
        return { 
            "success": True,
            "message": "Producto modificado correctamente"
        }, 204

    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ProductoServices.ALLOWED_EXTENSIONS

    @staticmethod
    def subir_imagenes_producto(id_producto, imagenes, categoria, principales):

        base_path = os.path.join(current_app.root_path, 'static', 'images', categoria, f'producto_{id_producto}')
        os.makedirs(base_path, exist_ok=True)

        rutas = []

        for idx, imagen in enumerate(imagenes):
            if imagen and ProductoServices.allowed_file(imagen.filename):
                filename = secure_filename(imagen.filename)

                if not filename:
                    return {"success": False, "message": "Nombre de archivo no válido."}, 400

                carpeta = f"buildify/productos/{categoria}/producto_{id_producto}"

                try:
                    cloudinary.config(
                        cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
                        api_key=current_app.config.get("CLOUDINARY_API_KEY"),
                        api_secret=current_app.config.get("CLOUDINARY_API_SECRET")
                    )

                    upload_result = cloudinary.uploader.upload(
                        imagen,
                        folder=carpeta,
                        use_filename=True,
                        unique_filename=False
                    )
                except Exception as e:
                    current_app.logger.error(f"Error al subir imagen: {e}")
                    return {"success": False, "message": "Error al subir imagen a Cloudinary."}, 500

                url = upload_result.get("secure_url")
                if not url:
                    return {"success": False, "message": "No se pudo obtener la URL de Cloudinary."}, 500

                imagen_db = ImagenesProducto(
                    nombre_archivo=url,
                    es_principal=(principales[idx].lower() == 'true'),
                    id_producto=int(id_producto)
                )
                db.session.add(imagen_db)
                rutas.append(url)
            else:
                return {"success": False, "message": "Archivo no válido."}, 400

        db.session.commit()
        return {"success": True, "imagenes_guardadas": rutas}, 201
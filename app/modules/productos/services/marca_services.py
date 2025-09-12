from app.modules.productos.models import Marca
from app import db

class MarcaService:

    @staticmethod
    def get_all_marcas():
        marcas = Marca.query.all()
        return [{"id_marca": m.id_marca, "nombre": m.nombre} for m in marcas]

    @staticmethod
    def get_marca_by_id(id_marca):
        marca = Marca.query.get_or_404(id_marca, description="Marca no encontrada.")
        return {"id_marca": marca.id_marca, "nombre": marca.nombre}

    @staticmethod
    def create_marca(nombre):
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()
        return {"id_marca": nueva_marca.id_marca, "nombre": nueva_marca.nombre}

    @staticmethod
    def update_marca(id_marca, nombre):
        marca = Marca.query.get_or_404(id_marca, description="Marca no encontrada.")
        marca.nombre = nombre
        db.session.commit()
        return {"id_marca": marca.id_marca, "nombre": marca.nombre}

    @staticmethod
    def delete_marca(id_marca):
        marca = Marca.query.get_or_404(id_marca, description="Marca no encontrada.")
        db.session.delete(marca)
        db.session.commit()
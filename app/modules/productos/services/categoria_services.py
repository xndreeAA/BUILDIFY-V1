from app.modules.productos.models import Categoria
from app import db

class CategoriaService:

    @staticmethod
    def get_all_categorias():
        categorias = Categoria.query.all()
        return [{"id_categoria": c.id_categoria, "nombre": c.nombre} for c in categorias]

    @staticmethod
    def get_categoria_by_id(id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria, description="Categoría no encontrada.")
        return {"id_categoria": categoria.id_categoria, "nombre": categoria.nombre}

    @staticmethod
    def create_categoria(nombre):
        nueva_categoria = Categoria(nombre=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()
        return {"id_categoria": nueva_categoria.id_categoria, "nombre": nueva_categoria.nombre}

    @staticmethod
    def update_categoria(id_categoria, nombre):
        categoria = Categoria.query.get_or_404(id_categoria, description="Categoría no encontrada.")
        categoria.nombre = nombre
        db.session.commit()
        return {"id_categoria": categoria.id_categoria, "nombre": categoria.nombre}

    @staticmethod
    def delete_categoria(id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria, description="Categoría no encontrada.")
        db.session.delete(categoria)
        db.session.commit()

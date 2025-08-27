from app import db

class ImagenesProducto(db.Model):
    __tablename__ = 'imagenes_producto'

    id_imagen_producto = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    es_principal = db.Column(db.Boolean, nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)

    def __repr__(self):
        return f'<ImagenesProducto archivo={self.nombre_archivo}>'

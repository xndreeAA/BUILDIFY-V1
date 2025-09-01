from app import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    id_marca = db.Column(db.Integer, db.ForeignKey('marcas.id_marca'), nullable=False)
    descripcion = db.Column(db.Text)

    detalles_chasis = db.relationship('DetalleChasis', backref='producto', uselist=False, cascade='all, delete')
    detalles_fuente_poder = db.relationship('DetalleFuentePoder', backref='producto', uselist=False, cascade='all, delete')
    detalles_memoria_ram = db.relationship('DetalleMemoriaRAM', backref='producto', uselist=False, cascade='all, delete')
    detalles_placa_base = db.relationship('DetallePlacaBase', backref='producto', uselist=False, cascade='all, delete')
    detalles_procesador = db.relationship('DetalleProcesador', backref='producto', uselist=False, cascade='all, delete')
    detalles_refrigeracion = db.relationship('DetalleRefrigeracion', backref='producto', uselist=False, cascade='all, delete')
    detalles_tarjeta_grafica = db.relationship('DetalleTarjetaGrafica', backref='producto', uselist=False, cascade='all, delete')
    imagenes = db.relationship('ImagenesProducto', backref='producto', cascade='all, delete', lazy=True)
    
    productos_pedidos = db.relationship(
        'ProductoPedido', back_populates='producto', passive_deletes=True
    )

    @property
    def imagen_principal(self):
        return next((img for img in self.imagenes if img.es_principal), None)
    
    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": float(self.precio),
            "stock": self.stock,
            "categoria": self.categoria.nombre,
            "marca": self.marca.nombre,
            "imagenes": [
                {
                    "ruta": imagen.nombre_archivo,
                    "es_principal": imagen.es_principal
                }
                for imagen in self.imagenes
            ]
        }

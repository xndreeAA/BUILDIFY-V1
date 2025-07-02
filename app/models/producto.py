from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    
    productos = db.relationship('Producto', backref='categoria', lazy=True)
    
    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class Marca(db.Model):
    __tablename__ = 'marcas'
    
    id_marca = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    
    productos = db.relationship('Producto', backref='marca', lazy=True)
    
    categorias = db.relationship(
        'Categoria',
        secondary='marcas_categorias',
        backref=db.backref('marcas', lazy='dynamic')
    )
    
    def __repr__(self):
        return f'<Marca {self.nombre}>'

class MarcaCategoria(db.Model):
    __tablename__ = 'marcas_categorias'
    
    id_marca_categoria = db.Column(db.Integer, primary_key=True)
    id_marca = db.Column(db.Integer, db.ForeignKey('marcas.id_marca'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    
    def __repr__(self):
        return f'<MarcaCategoria marca={self.id_marca} categoria={self.id_categoria}>'
    
class ImagenesProducto(db.Model):
    __tablename__ = 'imagenes_producto'

    id_imagen_producto = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    es_principal = db.Column(db.Boolean, nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)

    def __repr__(self):
        return f'<ImagenesProducto archivo={self.nombre_archivo}>'


class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    id_marca = db.Column(db.Integer, db.ForeignKey('marcas.id_marca'), nullable=False)

    imagenes = db.relationship('ImagenesProducto', backref='producto', lazy=True)

    @property
    def imagen_principal(self):
        return next((img for img in self.imagenes if img.es_principal), None)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

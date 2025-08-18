from app import db

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

from app import db

class Carrito(db.Model):
    __tablename__ = 'carritos'

    id_carrito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    
    usuario = db.relationship('Usuario', backref=db.backref('carritos', lazy=True))
    items = db.relationship('ItemCarrito', backref='carrito', cascade='all, delete-orphan', lazy=True)

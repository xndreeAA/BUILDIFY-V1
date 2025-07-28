from app import db

class Carrito(db.Model):
    __tablename__ = 'carritos'

    id_carrito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    
    usuario = db.relationship('Usuario', backref=db.backref('carritos', lazy=True))
    items = db.relationship('ItemCarrito', backref='carrito', cascade='all, delete-orphan', lazy=True)

class ItemCarrito(db.Model):
    __tablename__ = 'items_carrito'

    id_carrito = db.Column(db.Integer, db.ForeignKey('carritos.id_carrito'), primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto', ondelete='CASCADE'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Producto', backref=db.backref('items_carrito', passive_deletes=True))

    def to_dict(self):
        producto = self.producto.to_dict()
        producto['cantidad'] = self.cantidad
        producto["subtotal"] = float(self.producto.precio * self.cantidad)
        return producto
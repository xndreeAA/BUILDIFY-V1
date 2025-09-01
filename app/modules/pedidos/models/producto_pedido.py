from app import db

class ProductoPedido(db.Model):
    __tablename__ = 'productos_pedidos'

    id_producto_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto', ondelete="CASCADE"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    
    producto = db.relationship('Producto', back_populates='productos_pedidos', lazy=True)
from app import db

class Estado(db.Model):
    __tablename__ = 'estados'

    id_estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(100), unique=True, nullable=False)

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_pedido = db.Column(db.Date, nullable=False)
    fecha_entrega = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estados.id_estado'), nullable=False)

    usuario = db.relationship('Usuario', backref='pedidos', lazy=True)
    estado = db.relationship('Estado', backref='pedidos', lazy=True)

    productos_pedidos = db.relationship('ProductoPedido', backref='pedido', cascade='all, delete-orphan', lazy=True)

class ProductoPedido(db.Model):
    __tablename__ = 'productos_pedidos'

    id_producto_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Producto', backref='productos_pedidos', lazy=True)

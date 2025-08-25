from app import db

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_pedido = db.Column(db.DateTime, nullable=False)
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estados.id_estado'), nullable=False)

    usuario = db.relationship('Usuario', backref='pedidos', lazy=True)
    estado = db.relationship('Estado', backref='pedidos', lazy=True)
    productos_pedidos = db.relationship('ProductoPedido', backref='pedido', cascade='all, delete-orphan', lazy=True)
    factura = db.relationship('Factura', backref='pedido', lazy=True, uselist=False)
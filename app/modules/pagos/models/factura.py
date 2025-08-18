from app import db

class Factura(db.Model):
    __tablename__ = 'facturas'

    id_factura = db.Column(db.String(255), primary_key=True, nullable=False)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido', ondelete='SET NULL'))
    numero_factura = db.Column(db.String(100), nullable=False, unique=True)
    factura_url_invoice_stripe = db.Column(db.String(2083), nullable=False)
    factura_url_pdf_stripe = db.Column(db.String(2083))
    factura_url_pdf_cloud = db.Column(db.String(2083))
    total = db.Column(db.BigInteger, nullable=False)
    moneda = db.Column(db.CHAR(3), nullable=False)

    pedido = db.relationship('Pedido', backref=db.backref('facturas', lazy=True))
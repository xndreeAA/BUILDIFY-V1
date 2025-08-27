from supabase import create_client, Client
from flask import current_app
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

    def to_dict(self):

        supabase = create_client(current_app.config.get('SUPABASE_URL'), current_app.config.get('SUPABASE_SERVICE_ROLE_KEY'))
        
        signed_url = None
        if self.factura_url_pdf_cloud:
            try:
                signed_url_response = supabase.storage.from_('facturas').create_signed_url(
                    path=self.factura_url_pdf_cloud,
                    expires_in=1300
                )
                signed_url = signed_url_response.get('signedUrl')
                print(f"[DEBUG] Signed URL for {self.factura_url_pdf_cloud}: {signed_url}")
            except Exception as e:
                print(f"[ERROR] Failed to generate signed URL for {self.factura_url_pdf_cloud}: {str(e)}")

        return {
            'id_factura': self.id_factura,
            'id_pedido': self.id_pedido,
            'numero_factura': self.numero_factura,
            'factura_url_invoice_stripe': self.factura_url_invoice_stripe,
            'factura_url_pdf_stripe': self.factura_url_pdf_stripe,
            'factura_url_pdf_cloud': signed_url,
            'total': self.total,
            'moneda': self.moneda
        }
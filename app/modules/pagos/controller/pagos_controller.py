import stripe
from flask import jsonify, request, abort, current_app
from flask_login import current_user
from app.modules.pagos.services.pagos_services import PagosServices

class PagosController:

    @staticmethod
    def create_checkout_session(*args, **kwargs):
        id_usuario = current_user.get_id() if current_user.is_authenticated else None
        
        if not id_usuario:
            return jsonify({"error": "No autenticado."}), 401
        
        data, status = PagosServices.create_checkout_session(id_usuario)
        return jsonify(data), status

    
    @staticmethod
    def descargar_factura(*args, **kwargs):

        token = request.cookies.get("factura_token")
    
        if not token:
            return jsonify({"error": "No autorizado"}), 401

        return PagosServices.descargar_factura(token)
    
    @staticmethod
    def webhook(*args, **kwargs):        
        payload = request.data
        sig_header = request.headers.get('stripe-signature')
        webhook_secret = current_app.config.get('STRIPE_WEBHOOK_KEY')
        stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

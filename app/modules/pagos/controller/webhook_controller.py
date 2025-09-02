from flask import request, jsonify
from app.modules.pagos.services.webhook_services import WebhookService

class WebhookController:

    @staticmethod
    def webhook(*args, **kwargs):
        payload = request.data
        sig_header = request.headers.get("stripe-signature")

        success, status = WebhookService.handle_webhook(payload, sig_header)
        return jsonify(success=success), status

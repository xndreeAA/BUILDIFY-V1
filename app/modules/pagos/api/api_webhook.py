from flask import Blueprint
from app.modules.pagos.controller.webhook_controller import WebhookController

webhook_api_bp = Blueprint('webhook_api', __name__, url_prefix='/checkout/webhook')
webhook_api_bp.add_url_rule("", view_func=WebhookController.webhook, methods=["POST"])

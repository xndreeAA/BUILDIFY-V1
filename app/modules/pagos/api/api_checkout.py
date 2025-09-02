from flask import Blueprint

from app.modules.pagos.controller.pagos_controller import PagosController

checkout_api_bp = Blueprint('checkout_api', __name__, url_prefix='/checkout')

checkout_api_bp.add_url_rule("/create-checkout-session", view_func=PagosController.create_checkout_session, methods=["POST"])
checkout_api_bp.add_url_rule("/descargar-factura", view_func=PagosController.descargar_factura, methods=["GET"])
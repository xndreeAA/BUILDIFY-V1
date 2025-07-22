from flask import Blueprint, jsonify, request, abort, current_app
from flask_login import login_required, current_user
from app.models.usuario import Usuario
from app.models.carrito import Carrito, ItemCarrito
from app.models.producto import Producto
from sqlalchemy.orm import joinedload
import stripe

from app.config import DevelopmentConfig

stripe.api_key = DevelopmentConfig.STRIPE_SECRET_KEY
STRIPE_WEBHOOK_KEY = DevelopmentConfig.STRIPE_WEBHOOK_KEY

checkout_api_bp = Blueprint('checkout_api', __name__, url_prefix='/api/checkout')

@checkout_api_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    id_usuario = current_user.get_id() if current_user.is_authenticated else None
    if not id_usuario:
        abort(401, description="No autenticado.")

    usuario = Usuario.query.get_or_404(id_usuario, description="Usuario no encontrado.")
    carrito = Carrito.query.filter_by(id_usuario=usuario.id_usuario).first()

    if not carrito:
        return jsonify({"error": "El carrito no existe."}), 400
    
    items = ItemCarrito.query.options(
        joinedload(ItemCarrito.producto).joinedload(Producto.imagenes),
        joinedload(ItemCarrito.producto).joinedload(Producto.categoria),
        joinedload(ItemCarrito.producto).joinedload(Producto.marca)
    ).filter_by(id_carrito=carrito.id_carrito).all()

    items_serializados = [item.to_dict() for item in items]
    if not items_serializados:
        return jsonify({"error": "El carrito está vacío."}), 400

    line_items = []

    for item in items_serializados:
        line_items.append({
            'price_data': {
                'currency': 'COP',
                'product_data': {
                    'name': item['nombre'],
                    
                    ## Disable due to Stripe image management
                    # 'images': [f"{DevelopmentConfig.STATIC_URL}/{item['imagenes'][0]['ruta']}"] if item['imagenes'] else [],
                },
                'unit_amount': int(item['precio'] * 100),
            },
            
            'quantity': item['cantidad'],
        })

    try :
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            metadata={
                'id_usuario': usuario.id_usuario,
                'id_carrito': carrito.id_carrito
            },
            success_url= DevelopmentConfig.STRIPE_SUCCESS_URL or "http://localhost:5000/success",
            cancel_url= DevelopmentConfig.STRIPE_CANCEL_URL or "http://localhost:5000/cancel",
        )
        return jsonify({'url': checkout_session.url}), 200
    
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    
from flask import Blueprint, json, jsonify, request, abort, current_app
from flask_login import login_required, current_user
from app.core.models.usuario import Usuario
from app.modules.carrito.models.carrito import Carrito
from app.modules.carrito.models.item_carrito import ItemCarrito
from app.modules.productos.models.producto import Producto
from sqlalchemy.orm import joinedload
from datetime import datetime
import stripe

checkout_api_bp = Blueprint('checkout_api', __name__, url_prefix='/checkout')

@checkout_api_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    STRIPE_SECRET_KEY = current_app.config.get('STRIPE_SECRET_KEY')
    STRIPE_SUCCESS_URL = current_app.config.get('STRIPE_SUCCESS_URL')
    STRIPE_CANCEL_URL = current_app.config.get('STRIPE_CANCEL_URL')

    stripe.api_key = STRIPE_SECRET_KEY

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
                "productos_pedidos": json.dumps([
                    {"id_producto": item["id_producto"], "cantidad": item["cantidad"]} 
                    for item in items_serializados
                ]),
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "total": str(sum(item["precio"] * item["cantidad"] for item in items_serializados))
            },
            success_url= STRIPE_SUCCESS_URL or "http://localhost:5000/pagos/success",
            cancel_url=  STRIPE_CANCEL_URL or "http://localhost:5000/pagos/cancel",
        )

        return jsonify({'url': checkout_session.url}), 200
    
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    
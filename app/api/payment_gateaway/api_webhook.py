from flask import Blueprint, jsonify, json, request, abort, current_app
from app.models.pedidos import Pedido, ProductoPedido, Estado
from app.models.producto import Producto
from app.models.carrito import Carrito
from app import db
from datetime import datetime
import stripe

webhook_api_bp = Blueprint('webhook_api', __name__, url_prefix='/api/checkout/webhook')

@webhook_api_bp.route('', methods=['POST'])
def webhook():

    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    webhook_secret = current_app.config.get('STRIPE_WEBHOOK_KEY')
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

    try:
        event = stripe.Webhook.construct_event(
            payload, 
            sig_header=sig_header, 
            secret=webhook_secret
        )
    except ValueError as e:
        print('[ERROR] Invalid payload', e)
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        print('[ERROR] Invalid signature', e)
        return jsonify(success=False), 400
    except stripe.error.InvalidRequestError as e:
        print('[ERROR] Invalid request', e)
        return jsonify(success=False), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_completed(session)

    return jsonify(success=True), 200

def handle_checkout_completed(session):
    metadata = session.get('metadata', {})
    
    id_usuario = metadata.get('id_usuario')
    productos_pedidos_json = metadata.get('productos_pedidos')
    fecha = metadata.get('fecha')
    total = float(metadata.get('total')) 

    if not id_usuario or not productos_pedidos_json or not fecha or not total:
        print('[ERROR] Missing metadata in session')
        return

    try: 
        productos_pedidos = json.loads(productos_pedidos_json)
    except Exception as e:
        print('[ERROR] Could not parse productos JSON', e)
        return
    
    carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
    if carrito:
        carrito.items.clear()
        db.session.commit()

    crear_pedido(id_usuario, productos_pedidos, fecha, total)


def crear_pedido(id_usuario, productos_pedidos, fecha, total):
    try: 
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S").date()

        nuevo_pedido = Pedido(
            id_usuario=id_usuario,
            fecha_pedido=fecha_dt,
            fecha_entrega=fecha_dt,
            valor_total=total,
            id_estado=1
        )

        db.session.add(nuevo_pedido)
        db.session.flush()

        for producto in productos_pedidos:
            producto_db = Producto.query.get(producto["id_producto"])
            if not producto_db:
                print(f"[ERROR] Producto ID {producto['id_producto']} no encontrado")
                db.session.rollback()
                return

            if producto_db.stock < producto["cantidad"]:
                print(f"[ERROR] Stock insuficiente para producto {producto_db.id_producto}")
                db.session.rollback()
                return

            nuevo_producto_pedido = ProductoPedido(
                id_pedido=nuevo_pedido.id_pedido,
                id_producto=producto["id_producto"],
                cantidad=producto["cantidad"]
            )

            db.session.add(nuevo_producto_pedido)
            producto_db.stock -= producto["cantidad"]

            print(f"[INFO] Producto {producto_db.id_producto} stock actualizado a {producto_db.stock}")

        db.session.commit()
        print('[INFO] Pedido y productos guardados correctamente')
        print('[INFO] Pedido: ', nuevo_pedido )
    except Exception as e:
        db.session.rollback()
        print('[ERROR] Could not create order', e)
        return

import json
import stripe
from flask import current_app
import requests
from datetime import datetime
from supabase import create_client
from app import db
from app.modules.pedidos.models import Pedido, ProductoPedido, Estado
from app.modules.productos.models.producto import Producto
from app.modules.carrito.models.carrito import Carrito
from app.modules.pagos.models.factura import Factura

class WebhookService:

    @staticmethod
    def handle_webhook(payload, sig_header):
        webhook_secret = current_app.config.get("STRIPE_WEBHOOK_KEY")
        stripe.api_key = current_app.config.get("STRIPE_SECRET_KEY")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            print("[ERROR] Invalid payload", e)
            return False, 400
        except stripe.error.SignatureVerificationError as e:
            print("[ERROR] Invalid signature", e)
            return False, 400
        except stripe.error.InvalidRequestError as e:
            print("[ERROR] Invalid request", e)
            return False, 400

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            id_pedido = WebhookService.handle_checkout_completed(session)

            if id_pedido and session.get("invoice"):
                id_usuario = session["metadata"]["id_usuario"]
                invoice = stripe.Invoice.retrieve(session["invoice"])

                res = WebhookService.guardar_factura(invoice, id_pedido, id_usuario)
                if not res:
                    return False, 400

                email = session["customer_details"]["email"]
                WebhookService.send_factura_email(invoice, id_pedido, email)

        return True, 200


    @staticmethod
    def handle_checkout_completed(session):
        metadata = session.get("metadata", {})

        id_usuario = metadata.get("id_usuario")
        productos_pedidos_json = metadata.get("productos_pedidos")
        fecha = metadata.get("fecha")
        total = float(metadata.get("total"))
        session_id = session.get("id")

        if not id_usuario or not productos_pedidos_json or not fecha or not total:
            print("[ERROR] Missing metadata in session")
            return

        try:
            productos_pedidos = json.loads(productos_pedidos_json)
        except Exception as e:
            print("[ERROR] Could not parse productos JSON", e)
            return

        carrito = Carrito.query.filter_by(id_usuario=id_usuario).first()
        if carrito:
            carrito.items.clear()
            db.session.commit()

        return WebhookService.crear_pedido(
            id_usuario, productos_pedidos, fecha, total, session_id
        )


    @staticmethod
    def crear_pedido(id_usuario, productos_pedidos, fecha, total, session_id):
        try:
            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")

            nuevo_pedido = Pedido(
                id_usuario=id_usuario,
                fecha_pedido=fecha_dt,
                fecha_entrega=fecha_dt,
                valor_total=total,
                id_estado=1,
                stripe_session_id=session_id,
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
                    print(
                        f"[ERROR] Stock insuficiente para producto {producto_db.id_producto}"
                    )
                    db.session.rollback()
                    return

                nuevo_producto_pedido = ProductoPedido(
                    id_pedido=nuevo_pedido.id_pedido,
                    id_producto=producto["id_producto"],
                    cantidad=producto["cantidad"],
                )

                db.session.add(nuevo_producto_pedido)
                producto_db.stock -= producto["cantidad"]

                print(
                    f"[INFO] Producto {producto_db.id_producto} stock actualizado a {producto_db.stock}"
                )

            db.session.commit()
            print("[INFO] Pedido y productos guardados correctamente")
            return nuevo_pedido.id_pedido

        except Exception as e:
            db.session.rollback()
            print("[ERROR] Could not create order", e)
            return


    @staticmethod
    def guardar_factura(invoice, id_pedido, id_usuario):
        SUPABASE_URL = current_app.config.get("SUPABASE_URL")
        SUPABASE_SERVICE_ROLE_KEY = current_app.config.get("SUPABASE_SERVICE_ROLE_KEY")

        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        file_path = f"{str(id_usuario)}/factura_{invoice.id}.pdf"

        try:
            pdf_response = requests.get(invoice.invoice_pdf)
            pdf_response.raise_for_status()
            pdf_bytes = pdf_response.content

            supabase.storage.from_("facturas").upload(
                path=file_path,
                file=pdf_bytes,
                file_options={"content-type": "application/pdf", "upsert": "true"},
            )

            nueva_factura = Factura(
                id_factura=invoice.id,
                id_pedido=id_pedido,
                numero_factura=invoice.number,
                factura_url_invoice_stripe=invoice.hosted_invoice_url,
                factura_url_pdf_stripe=invoice.invoice_pdf,
                factura_url_pdf_cloud=file_path,
                total=invoice.total,
                moneda=invoice.currency,
            )

            db.session.add(nueva_factura)
            db.session.commit()

            print(
                f"[INFO] Factura {invoice.id} guardada y subida a Supabase para pedido {id_pedido}"
            )
            return True

        except Exception as e:
            print(f"[ERROR] Could not create factura: {str(e)}")
            db.session.rollback()
            return False


    @staticmethod
    def send_factura_email(invoice, id_pedido, email):
        # 🔹 Implementar tu lógica real de envío de correo
        print(f"[INFO] Enviando factura {invoice.id} al email {email}")

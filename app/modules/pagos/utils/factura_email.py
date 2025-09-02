from flask_mail import Message
from flask import current_app, render_template
from app import mail
import requests

def send_factura_email(invoice, id_pedido, email):
    try:
        pdf_response = requests.get(invoice.invoice_pdf)
        pdf_response.raise_for_status()
        pdf_bytes = pdf_response.content

        msg = Message(
            subject=f'Factura de tu compra #{id_pedido}',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        msg.html = render_template(
            "email-factura.html",
            hosted_url=invoice.hosted_invoice_url,
            invoice_number=invoice.number,
            customer_name=invoice.customer_name, 
            id_pedido=id_pedido
        )

        msg.attach(
            filename=f"factura_{invoice.id}.pdf",
            content_type="application/pdf",
            data=pdf_bytes
        )

        mail.send(msg)

        print(f"[INFO] Factura enviada a {email} con HTML para pedido {id_pedido}")
        return True

    except Exception as e:
        print("[ERROR] No se pudo enviar la factura:", e)
        return False

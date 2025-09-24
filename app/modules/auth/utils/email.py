from flask import url_for, current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_reset_email(usuario):
    print("✅ Entrando a send_reset_email con SendGrid...")

    # Genera el token
    token = usuario.get_reset_token()
    print(f"✅ Token generado: {token}")

    # Construye el link
    link = url_for('web_v1.auth.reset_password', token=token, _external=True)
    print(f"✅ Link generado: {link}")

    # Crear el correo
    message = Mail(
        from_email=os.getenv("SENDGRID_SENDER"),
        to_emails=usuario.email,
        subject='Restablecer contraseña',
        plain_text_content=f'''Hola 👋 {usuario.nombre},

Hemos recibido una solicitud para restablecer tu contraseña en Buildify. Si fuiste tú quien la solicitó, haz clic en el siguiente enlace:

🪄 {link}

Este enlace estará disponible por un tiempo limitado.

Si no solicitaste este cambio, puedes ignorar este mensaje.

Gracias por confiar en nosotros.😊✌️

Atentamente,
El equipo Buildify
'''
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"✅ Correo enviado con status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")

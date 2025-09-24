from flask_mail import Message
from flask import url_for, current_app
from app import mail

# Correo generico para restablecer la contraseña
def send_reset_email(usuario):
    print("✅ Entrando a send_reset_email...")  # <-- Debug inicial

    # Genera el token para restablecimiento de contraseña
    token = usuario.get_reset_token()
    print(f"✅ Token generado: {token}")  # <-- Debug token
    
    # Construye el enlace absoluto con el token
    link = url_for('web_v1.auth.reset_password', token=token, _external=True)
    print(f"✅ Link generado: {link}")  # <-- Debug link

    # Crea el mensaje del correo
    msg = Message(
        subject='Restablecer contraseña',
        sender=current_app.config['MAIL_USERNAME'],  # Usa el remitente desde la config
        recipients=[usuario.email]
    )
    print(f"✅ Mensaje creado para: {usuario.email}")  # <-- Debug mensaje

    # Cuerpo del correo (texto plano)
    msg.body = f'''Hola 👋 {usuario.nombre},

Hemos recibido una solicitud para restablecer tu contraseña en Buildify. Si fuiste tú quien la solicitó, por favor haz clic en el siguiente enlace para continuar con el proceso:

🪄{link}

Este enlace estará disponible por un tiempo limitado por motivos de seguridad.

Si no solicitaste este cambio, puedes ignorar este mensaje con total tranquilidad. Tu información permanece segura.

Gracias por confiar en nosotros.😊✌️

Atentamente,
El equipo Buildify
'''

    msg.charset = 'utf-8'  # ✅ Forzar codificación UTF-8
    print("✅ Cuerpo del mensaje creado.")  # <-- Debug cuerpo

    # Envía el correo
    print("🚀 Intentando enviar correo...")  # <-- Debug antes de enviar
    mail.send(msg)
    print("✅ Correo enviado exitosamente.")  # <-- Debug después de enviar

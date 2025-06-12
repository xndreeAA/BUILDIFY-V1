from flask_mail import Message
from flask import url_for, current_app
from app import mail

def send_reset_email(usuario):
    # Genera el token para restablecimiento de contraseña
    token = usuario.get_reset_token()
    
    # Construye el enlace absoluto con el token
    link = url_for('auth.reset_password', token=token, _external=True)

    # Crea el mensaje del correo
    msg = Message(
        subject='Restablecer contraseña',
        sender=current_app.config['MAIL_USERNAME'],  # Usa el remitente desde la config
        recipients=[usuario.email]
    )

    # Cuerpo del correo (texto plano)
    msg.body = f'''Hola {usuario.nombre},

Para restablecer tu contraseña, haz clic en el siguiente enlace:

{link}

Si tú no solicitaste esto, simplemente ignora este correo.

Atentamente,
El equipo de soporte
'''

    msg.charset = 'utf-8'  # ✅ Forzar codificación UTF-8

    # Envía el correo
    mail.send(msg)

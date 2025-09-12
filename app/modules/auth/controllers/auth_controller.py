from flask import render_template, request, redirect, url_for, flash, session, make_response
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token, set_access_cookies

from app.core.models.usuario import Usuario
from app.modules.auth.forms.login_form import LoginForm
from app.modules.auth.forms.register_form import RegisterForm
from app.modules.auth.forms.forgot_password_form import ForgotPasswordForm
from app.modules.auth.forms.reset_password_form import ResetPasswordForm
from app.modules.auth.utils.email import send_reset_email

from app import db
from datetime import timedelta
import time

MAX_INTENTOS = 5
TIEMPO_BLOQUEO = 60

# ------------------ LOGIN ------------------ #
def login():

    form = LoginForm()

    intentos = session.get('intentos_login', 0)
    ultimo_intento = session.get('ultimo_login', 0)

    if intentos >= MAX_INTENTOS and time.time() - ultimo_intento < TIEMPO_BLOQUEO:
        flash('Demasiados intentos fallidos. Intenta nuevamente en 1 minuto.', 'danger')
        return render_template('login.html', form=form)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            session.pop('intentos_login', None)
            session.pop('ultimo_login', None)

            token = generar_token(usuario.id_usuario)

            if usuario.rol == 'administrador':
                resp = make_response(redirect(url_for('web_v1.admin.dashboard')))
            elif usuario.rol == 'moderador':
                resp = make_response(redirect(url_for('web_v1.admin.dashboard')))
            elif usuario.rol == 'usuario':
                resp = make_response(redirect(url_for('web_v1.user.home')))
            else:
                flash('Rol de usuario no autorizado.', 'danger')
                return redirect(url_for('web_v1.auth.login'))

            set_access_cookies(resp, token)
            return resp

        session['intentos_login'] = intentos + 1
        session['ultimo_login'] = time.time()
        flash('Credenciales incorrectas.', 'danger')

    return render_template('login.html', form=form)


def generar_token(id_usuario):
    claims = {"user_id": id_usuario}
    token = create_access_token(
        identity=str(id_usuario),
        additional_claims=claims,
        expires_delta=timedelta(hours=2)
    )
    return token

# ------------------ LOGOUT ------------------ #
def logout():
    logout_user()
    return redirect(url_for('web_v1.auth.login'))

# ------------------ REGISTER ------------------ #
def register():
    form = RegisterForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        existing_user = Usuario.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Ya existe un usuario con ese correo.', 'danger')
            return render_template('register.html', form=form)

        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            id_rol=1
        )
        nuevo_usuario.set_password(form.password.data)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('web_v1.auth.register'))

    return render_template('register.html', form=form)

# ------------------ OLVIDÉ MI CONTRASEÑA ------------------ #
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario:
            send_reset_email(usuario)
        flash('Si el correo está registrado, recibirás instrucciones para restablecer tu contraseña.', 'info')
        return redirect(url_for('web_v1.auth.login'))
    
    return render_template('forgot_password.html', form=form)

# ------------------ RESETEAR CONTRASEÑA CON TOKEN ------------------ #
def reset_password(token):
    usuario = Usuario.verify_reset_token(token)
    if not usuario:
        flash('El enlace es inválido o ha expirado.', 'danger')
        return redirect(url_for('web_v1.auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        usuario.set_password(form.password.data)
        db.session.commit()
        flash('Tu contraseña ha sido actualizada. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('web_v1.auth.login'))

    return render_template('reset_password.html', form=form)

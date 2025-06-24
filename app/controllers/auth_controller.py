from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from app.models.usuario import Usuario
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.forgot_password_form import ForgotPasswordForm  # 📌 NUEVO
from app.forms.reset_password_form import ResetPasswordForm    # 📌 NUEVO
from app.utils.email import send_reset_email                   # 📌 NUEVO
from app import db
import time

# Constantes de seguridad evita ataques de fuerza bruta
MAX_INTENTOS = 5
TIEMPO_BLOQUEO = 60  # en segundos

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

            if usuario.rol == 'administrador':
                return redirect(url_for('admin.dashboard'))
            elif usuario.rol == 'colaborador':
                return redirect(url_for('colaborador.dashboard'))
            elif usuario.rol == 'usuario':
                return redirect(url_for('user.home'))
            else:
                flash('Rol de usuario no autorizado.', 'danger')
                return redirect(url_for('auth.login'))

        session['intentos_login'] = intentos + 1
        session['ultimo_login'] = time.time()
        flash('Credenciales incorrectas.', 'danger')

    return render_template('auth/login.html', form=form)

# ------------------ LOGOUT ------------------ #
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

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
            id_rol=1  # Por defecto "colaborador"
        )
        nuevo_usuario.set_password(form.password.data)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.register'))

    return render_template('auth/register.html', form=form)

# ------------------ OLVIDÉ MI CONTRASEÑA ------------------ #
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario:
            send_reset_email(usuario)
        flash('Si el correo está registrado, recibirás instrucciones para restablecer tu contraseña.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html', form=form)

# ------------------ RESETEAR CONTRASEÑA CON TOKEN ------------------ #
def reset_password(token):
    usuario = Usuario.verify_reset_token(token)
    if not usuario:
        flash('El enlace es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        usuario.set_password(form.password.data)
        db.session.commit()
        flash('Tu contraseña ha sido actualizada. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)

from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from app.models.usuario import Usuario
from app.forms.login_form import LoginForm
import time

# Constantes de seguridad evita ataques de fuerza bruta
MAX_INTENTOS = 5
TIEMPO_BLOQUEO = 60  # en segundos

def login():
    form = LoginForm()
    
    # Obtiene el número de intentos fallidos y la hora del último intento de sesión
    intentos = session.get('intentos_login', 0)
    ultimo_intento = session.get('ultimo_login', 0)

    # Verifica bloqueo temporal: si supera intentos
    if intentos >= MAX_INTENTOS and time.time() - ultimo_intento < TIEMPO_BLOQUEO:
        flash('Demasiados intentos fallidos. Intenta nuevamente en 1 minuto.', 'danger')
        return render_template('login.html', form=form)
    
    # Procesa el formulario solo si es válido y fue enviado por POST
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data 
        # Busca el usuario por email
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica si el usuario existe y la contraseña es correcta
        if usuario and usuario.check_password(password):
            login_user(usuario)
            # Limpia contador de intentos tras login exitoso
            session.pop('intentos_login', None)
            session.pop('ultimo_login', None)

            # Redirección basada en rol
            if usuario.rol == 'administrador':
                return redirect(url_for('admin.dashboard'))
            elif usuario.rol == 'colaborador':
                return redirect(url_for('colaborador.dashboard'))
            else:
                flash('Rol de usuario no autorizado.', 'danger')
                return redirect(url_for('auth.login'))

        # Credenciales incorrectas
        session['intentos_login'] = intentos + 1
        session['ultimo_login'] = time.time()
        flash('Credenciales incorrectas.', 'danger')

    return render_template('login.html', form=form)

def logout():
    logout_user() # Cierra la sesión del usuario actual
    return redirect(url_for('auth.login'))

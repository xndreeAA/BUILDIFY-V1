from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from app.models.usuario import Usuario
from app.forms.login_form import LoginForm
import time
from app.forms.register_form import RegisterForm
from app import db


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

def register():
    form = RegisterForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        existing_user = Usuario.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Ya existe un usuario con ese correo.', 'danger')
            return render_template('register.html', form=form)

        nuevo_usuario = Usuario(
            nombre=form.username.data,
            apellido=form.lastname.data,
            email=form.email.data,
            direccion=form.address.data,
            telefono=form.phone.data,
            id_rol=2  # Por defecto "colaborador"
        )
        nuevo_usuario.set_password(form.password.data)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)
 
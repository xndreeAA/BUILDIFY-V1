from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

# Decorador para restringir acceso solo a administradores
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'administrador':
            flash('Acceso restringido: solo para administradores.', 'danger')
            return redirect(url_for('web_v1.admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# Decorador para restringir acceso solo a colaboradores
def colaborador_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'colaborador':
            flash('Acceso restringido: solo para colaboradores.', 'danger')
            return redirect(url_for('web_v1.auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# Decorador para restringir acceso solo a usuarios normales
def usuario_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != 'usuario':
            flash('Acceso restringido: solo para usuarios.', 'danger')
            return redirect(url_for('web_v1.auth.login'))
        return f(*args, **kwargs)
    return decorated_function

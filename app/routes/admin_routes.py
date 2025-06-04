from flask import Blueprint, render_template
from flask_login import login_required, current_user

# ----- DEFINICIÓN DEL BLUEPRINT -----
# Crea un blueprint para las rutas del área de administración
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ----- RUTA: PANEL DE ADMINISTRACIÓN -----
@admin_bp.route('/dashboard')
@login_required  # Requiere que el usuario haya iniciado sesión
def dashboard():#funcion de dashboard
    
    #Muestra el panel principal del administrador.
    #Solo accesible para usuarios autenticados.
    
    return render_template('layout-admin/index.html', nombre=current_user.nombre)

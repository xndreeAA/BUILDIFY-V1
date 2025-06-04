from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Crea un blueprint para las rutas del área de colaboradores
colaborador_bp = Blueprint('colaborador', __name__, url_prefix='/colaborador')

@colaborador_bp.route('/dashboard')
@login_required
def dashboard():
    #Muestra el panel principal del colaborador.
    #Solo accesible para usuarios autenticados
    return render_template('colaborador_dashboard.html', nombre=current_user.nombre)

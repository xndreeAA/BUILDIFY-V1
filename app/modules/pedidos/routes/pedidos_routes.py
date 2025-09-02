from flask import Blueprint, render_template, redirect, url_for, flash
from app.modules.pagos.forms.checkout_form import CheckoutForm
from flask_login import login_required, current_user 
import os

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

pedidos_routes_bp = Blueprint(
    'pedidos',
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)

@pedidos_routes_bp.route('/mis_pedidos')
@login_required
def pedidos_usuario():
    return render_template('pedidos_usuario.html')
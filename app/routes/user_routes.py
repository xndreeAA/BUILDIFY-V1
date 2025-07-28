from flask import Blueprint
from flask import render_template, Blueprint
from flask_login import login_required, current_user 
from app.models.producto import Producto
import requests

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def home():
    return render_template('user/home.html')


@user_bp.route('/section/<category>')
def section(category):
    productos = Producto.query.join(Producto.categoria).filter_by(nombre=category).all()
    return render_template('user/section.html', products=productos, category=category)

# ----------------------------------------------------------------
@user_bp.route('/brand_view')
def brand_view():
    return render_template('user/brand_view.html')
# ----------------------------------------------------------------

@user_bp.route('/product_details')
def product_details():
    return render_template('user/product_details.html')

# ----------------------------------------------------------------

@user_bp.route('/carrito')
@login_required
def carrito():
    return render_template('user/carrito.html')
# ----------------------------------------------------------------
from app.forms.checkout_form import CheckoutForm

@user_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        # procesar datos
        pass
    return render_template('user/checkout.html', form=form)
# ----------------------------------------------------------------
#-------------------Rutas de perfil de usuario-------------------

@user_bp.route('/user_info')
@login_required
def user_info():
    return render_template('user/user_perfil/' + 'user_info.html')

@user_bp.route('/mi_perfil')
@login_required
def mi_perfil():
    return render_template('user/user_perfil/' + 'mi_perfil.html')

@user_bp.route('/mis_compras')
@login_required
def mis_compras():
    return render_template('user/user_perfil/' + 'mis_compras.html')

@user_bp.route('/estado_pedidos')
@login_required
def estado_pedidos():
    return render_template('user/user_perfil/' + 'estado_pedidos.html')

@user_bp.route('/configuracion_perfil')
@login_required
def configuracion_perfil():
    return render_template('user/user_perfil/' + 'configuracion_perfil.html')

# ------------------------------------------------------------------------
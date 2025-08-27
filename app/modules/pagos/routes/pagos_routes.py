from flask import Blueprint, render_template, redirect, url_for, flash
from app.modules.pagos.forms.checkout_form import CheckoutForm
import os

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

pagos_routes_bp = Blueprint(
    'pagos',
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)

@pagos_routes_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        flash("Pago realizado con éxito", "success")
        return redirect(url_for('pagos.success'))
    return render_template('checkout.html', form=form)

@pagos_routes_bp.route('/success')
def success():
    return render_template('/success.html')

@pagos_routes_bp.route('/cancel')
def cancel():
    return render_template('/cancel.html')

@pagos_routes_bp.route('/email-factura')
def email_factura():
    return render_template('/email-factura.html')
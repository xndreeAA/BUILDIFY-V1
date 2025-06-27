from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.checkout_form import CheckoutForm


checkout_bp = Blueprint('checkout', __name__)

@checkout_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        flash("Pago realizado con éxito", "success")
        return redirect(url_for('checkout.checkout'))
    return render_template('user/checkout.html', form=form)
from flask import Blueprint
from flask import render_template, Blueprint
from flask_login import login_required, current_user 
import requests
import os

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

carrito_routes_bp = Blueprint(
    'carrito',
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)

@carrito_routes_bp.route('/')
@login_required
def carrito():
    return render_template('carrito.html')
# app/routes/main_routes.py

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)  # NO uses url_prefix si quieres que sea raíz

@main_bp.route('/')
def home():
    return render_template('home/home.html')

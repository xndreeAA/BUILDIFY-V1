from flask import Blueprint
from app.modules.auth.controllers import auth_controller
from app.modules.auth.controllers.auth_controller import (
    login, logout, register, forgot_password, reset_password
)
import os
    
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
auth_routes_bp = Blueprint('auth', __name__, template_folder=template_dir)

auth_routes_bp.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
auth_routes_bp.add_url_rule('/logout', view_func=logout)
auth_routes_bp.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
auth_routes_bp.add_url_rule('/forgot-password', view_func=forgot_password, methods=['GET', 'POST'])
auth_routes_bp.add_url_rule('/reset-password/<token>', view_func=reset_password, methods=['GET', 'POST'])

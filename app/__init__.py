from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail 
from itsdangerous import URLSafeTimedSerializer 
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
jwt = JWTManager()

serializer = None

def create_app():
    load_dotenv()  
    app = Flask(__name__, template_folder='core/templates', static_folder='core/static')
    app.config.from_object('app.config.DevelopmentConfig')

    csrf = CSRFProtect()
    db.init_app(app) 
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)

    login_manager.login_view = 'web_v1.auth.login'

    global serializer
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    from app.core.models.usuario import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    

    from app.modules.pagos.api.api_checkout import checkout_api_bp
    from app.modules.pagos.api.api_webhook import webhook_api_bp
    from app.modules.usuarios.api.api_usuarios import usuarios_api_bp

    from .interfaces.api import api_v1
    from .interfaces.web import web_v1

    csrf.exempt(checkout_api_bp)
    csrf.exempt(webhook_api_bp)
    csrf.exempt(usuarios_api_bp)

    app.register_blueprint(api_v1)
    app.register_blueprint(web_v1)



    return app

__all__ = ['db', 'serializer']

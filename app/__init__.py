from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail 
from itsdangerous import URLSafeTimedSerializer 
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

serializer = None

def create_app():
    load_dotenv()  
    app = Flask(__name__, template_folder='core/templates')
    app.config.from_object('app.config.DevelopmentConfig')

    csrf = CSRFProtect()
    db.init_app(app) 
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'

    global serializer
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    from app.core.models.usuario import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # csrf.exempt(checkout_api_bp)
    # csrf.exempt(webhook_api_bp)

    from .api import api_v1
    from .web import web_v1
    
    app.register_blueprint(api_v1)
    app.register_blueprint(web_v1)

    return app

__all__ = ['db', 'serializer']

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

import os

# ----- INICIALIZACIÓN GLOBAL DE EXTENSIONES -----
# Estas instancias serán utilizadas dentro de la factory 'create_app'
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
  
    load_dotenv()  

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app) 
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from app.models.usuario import Usuario
    from app.models.rol import Rol
    

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.colaborador_routes import colaborador_bp

    from app.routes.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(colaborador_bp)
    app.register_blueprint(user_bp)
    
    return app

__all__ = ['db']



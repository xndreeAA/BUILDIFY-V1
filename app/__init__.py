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
    # Configura la app, inicializa extensiones y registra blueprints.
    
    load_dotenv()  # Cargar variables de entorno

    #----- CONFIGURACIÓN DE LA APLICACIÓN -----
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')# Cambiar a modo producción si es necesario

    # ----- INICIALIZACIÓN DE EXTENSIONES -----
    db.init_app(app) # Configura SQLAlchemy
    migrate.init_app(app, db) # Configura Flask-Migrate
    login_manager.init_app(app)# Configura Flask-Login

    login_manager.login_view = 'auth.login'#redirecciona, chequeo estatico

    # ✅ Importación diferida para evitar importaciones circulares
    from app.models.usuario import Usuario
    from app.models.rol import Rol
    

    @login_manager.user_loader
    def load_user(user_id):
        #requerido por Flask-Login para cargar el usuario desde el ID
        return Usuario.query.get(int(user_id))

    # ----- REGISTRO DE BLUEPRINTS ----- (rutas)
    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.colaborador_routes import colaborador_bp
    # Se registran las rutas de cada módulo en la aplicación principal
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(colaborador_bp)
    
    return app

# ----- EXPORTACIÓN PARA USO EXTERNO -----
# Permite importar 'db' desde otros módulos con: from app import db
__all__ = ['db']



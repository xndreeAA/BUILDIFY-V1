from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail 
from dotenv import load_dotenv

import os

# ✅ Importación agregada para el manejo de tokens seguros de recuperación
from itsdangerous import URLSafeTimedSerializer  

# ----- INICIALIZACIÓN GLOBAL DE EXTENSIONES -----
# Estas instancias serán utilizadas dentro de la factory 'create_app'
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()  # Para enviar correos electrónicos, si es necesario
# ✅ Variable global del serializador para generar y verificar tokens de recuperación
serializer = None  # Se asigna luego dentro de create_app


def create_app():
    # Configura la app, inicializa extensiones y registra blueprints.
    
    load_dotenv()  # Cargar variables de entorno

    #----- CONFIGURACIÓN DE LA APLICACIÓN -----
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')  # Cambiar a modo producción si es necesario

    # ----- INICIALIZACIÓN DE EXTENSIONES -----
    db.init_app(app)  # Configura SQLAlchemy
    migrate.init_app(app, db)  # Configura Flask-Migrate
    login_manager.init_app(app)  # Configura Flask-Login
    mail.init_app(app) # ✅ Inicializa Flask-Mail con la app
    
    login_manager.login_view = 'auth.login'  # redirecciona si no ha iniciado sesión

    # ✅ Inicializar serializador para tokens seguros de recuperación
    global serializer
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    # ✅ Importación diferida para evitar importaciones circulares
    from app.models.usuario import Usuario
    from app.models.rol import Rol

    @login_manager.user_loader
    def load_user(user_id):
        # Requerido por Flask-Login para cargar el usuario desde el ID
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
    # app.register_blueprint(user_bp)
    
    return app

# ----- EXPORTACIÓN PARA USO EXTERNO -----
# Permite importar 'db' desde otros módulos con: from app import db
__all__ = ['db', 'serializer']  # ✅ Exportar también el serializador para uso en funciones de email

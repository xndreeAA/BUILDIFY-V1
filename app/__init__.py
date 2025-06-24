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

    load_dotenv()  

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app) 
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'

    global serializer
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        
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
    
    # app.register_blueprint(user_bp)
    
    return app

# ----- EXPORTACIÓN PARA USO EXTERNO -----
# Permite importar 'db' desde otros módulos con: from app import db
__all__ = ['db', 'serializer']  # ✅ Exportar también el serializador para uso en funciones de email

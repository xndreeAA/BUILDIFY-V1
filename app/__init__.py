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
    app = Flask(__name__, template_folder='templates', static_folder='static')
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

    # MODELOS
    from app.models.usuario import Usuario
    from app.models.rol import Rol
    from app.models.producto import Producto, Categoria, Marca, MarcaCategoria
    from app.models.detalles_producto import (
        DetalleProcesador,
        DetalleTarjetaGrafica,
        DetalleMemoriaRAM,
        DetallePlacaBase,
        DetalleRefrigeracion,
        DetalleChasis,
        DetalleFuentePoder
    )

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # RUTAS
    from app.routes.auth_routes import auth_bp
    from app.routes.main_routes import main_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.colaborador_routes import colaborador_bp
    from app.routes.user_routes import user_bp
    from app.routes.checkout import checkout_bp

    # APIS
    from app.api.productos.api_productos import productos_bp
    from app.api.productos.api_marcas import marcas_bp
    from app.api.productos.api_categorias import categorias_bp
    from app.api.productos.api_detalles import detalles_bp
    from app.api.productos.api_carrito import carrito_bp
    from app.api.usuarios.api_usuarios import user_api_bp

    from app.api.payment_gateaway.api_checkout import checkout_api_bp
    from app.api.payment_gateaway.api_webhook import webhook_api_bp

    from app.api.pedidos.api_pedidos import pedidos_bp

    # REGISTRO BLUEPRINTS
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(colaborador_bp)
    app.register_blueprint(user_bp)

    app.register_blueprint(productos_bp)
    app.register_blueprint(marcas_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(detalles_bp)
    app.register_blueprint(carrito_bp)

    app.register_blueprint(user_api_bp)
    app.register_blueprint(checkout_bp)

    # PAYMENT GATEAWAY THAT ACTUALLY WORKS
    app.register_blueprint(checkout_api_bp)
    app.register_blueprint(webhook_api_bp)
    app.register_blueprint(pedidos_bp)
    
    csrf.exempt(checkout_api_bp)
    csrf.exempt(webhook_api_bp)

    return app

__all__ = ['db', 'serializer']

import os

class DevelopmentConfig:
    
# ----- Llave secreta -----
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-default')
    
# ----- Configuracion de la base de datos -----
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', 3405)
    DB_NAME = os.getenv('DB_NAME')
    STATIC_URL = os.getenv('BASE_STATIC_URL', '/static')

# ----- Configuracion URI de SQLALCHEMY -----
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# ----- Configuración de Flask-Mail -----
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

# ----- Configuración de Cookies -----
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

# ----- Configuración de Cloudinary -----
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# ----- Configuracion de Supabase -----
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# ----- Configuración de Stripe -----
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'MISSING_STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_KEY = os.getenv('STRIPE_WEBHOOK_KEY', 'MISSING_STRIPE_WEBHOOK_KEY')
    STRIPE_SUCCESS_URL = os.getenv('STRIPE_SUCCESS_URL')
    STRIPE_CANCEL_URL = os.getenv('STRIPE_CANCEL_URL')

# ----- Configuración de Cloudinary -----
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    CLOUDINARY_FOLDER = os.getenv('CLOUDINARY_FOLDER', 'buildify')



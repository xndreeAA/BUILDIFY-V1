import os

class DevelopmentConfig:
    #Configuración específica para el entorno de desarrollo.
    #Utiliza variables de entorno para mayor seguridad y flexibilidad.
    
    # ----- CLAVE SECRETA -----
    # Se usa para mantener la seguridad de las sesiones y formularios (CSRF)
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-default')
    
    # ----- PARÁMETROS DE BASE DE DATOS -----
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', 3306)
    DB_NAME = os.getenv('DB_NAME')

    # ----- URI DE CONEXIÓN -----
    # Construye la URI para conectar con MySQL utilizando PyMySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # ----- CONFIGURACIÓN DE SQLALCHEMY -----
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Desactiva el sistema de seguimiento para mejorar el rendimiento

'''Cuando se cambia a modo produccion se desactiva el modo de depuración 
y se asegura que la clave secreta sea obligatoria.
las COOKIES solo se envia por HTTPS y se protegen contra XSS.'''

# class ProductionConfig:
#     """Configuración segura para entornos de producción."""
    
#     # 🔐 Clave secreta (debe establecerse como variable de entorno segura)
#     SECRET_KEY = os.environ['SECRET_KEY']  # Sin valor por defecto, obligatorio

#     # ⚙️ Parámetros de base de datos
#     DB_USER = os.environ['DB_USER']
#     DB_PASSWORD = os.environ['DB_PASSWORD']
#     DB_HOST = os.environ['DB_HOST']
#     DB_PORT = os.getenv('DB_PORT', 3306)  # Puede tener default
#     DB_NAME = os.environ['DB_NAME']

#     SQLALCHEMY_DATABASE_URI = (
#         f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     )

#     # ⚠️ No seguimiento de modificaciones (mejor rendimiento)
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # ❌ Apagar el modo de depuración
#     DEBUG = False

#     # 🔐 Seguridad adicional (puedes ampliarla)
#     SESSION_COOKIE_SECURE = True     # Solo enviar cookies por HTTPS
#     REMEMBER_COOKIE_SECURE = True    # Igual para cookies de "recordar sesión"
#     SESSION_COOKIE_HTTPONLY = True   # Protección contra XSS
#     REMEMBER_COOKIE_HTTPONLY = True


from app import db  
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.rol import Rol  # Asegúrate de que esta ruta sea correcta

class Usuario(db.Model, UserMixin):
    """
    Modelo de usuario para autenticación y gestión de roles.
    Utiliza SQLAlchemy para el mapeo de la base de datos y Flask-Login para la sesión.
    """
    __tablename__ = 'usuarios'
    #Modelo de datos en python, para poder interactuar con la base de datos usando SQLAlchemy.
    #Proposito: mapear la tabla usuarios de la base de datos.
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15))
    password = db.Column(db.String(256), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))
    
    # Relación con la tabla roles
    rol_rel = db.relationship('Rol', backref='usuarios')

    # ----- MÉTODOS DE SEGURIDAD -----

    def set_password(self, password):
        #Hashea y guarda la contraseña.
        self.password = generate_password_hash(password)

    def check_password(self, password):
        #Verifica la contraseña hasheada.
        return check_password_hash(self.password, password)
    
    def get_id(self):
        #Devuelve el id del usuario como cadena de texto (requerido por Flask-Login).
        return str(self.id_usuario)

    @property
    def rol(self):
        #Devuelve el nombre del rol asociado al usuario o None si no tiene.
        return self.rol_rel.rol if self.rol_rel else None  


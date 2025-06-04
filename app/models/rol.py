from app import db

class Rol(db.Model):
    __tablename__ = 'roles' # Nombre de la tabla en la base de datos

    id_rol = db.Column(db.Integer, primary_key=True) # ID único del rol, clave primaria
    rol = db.Column(db.String(50), nullable=False) # Nombre del rol, campo obligatorio


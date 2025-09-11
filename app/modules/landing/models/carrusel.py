from app import db
from datetime import datetime

class Carrusel(db.Model):
    __tablename__ = 'carruseles'

    id_carrusel = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    # Campos para Cloudinary
    url_imagen = db.Column(db.String(500), nullable=True)  # secure_url
    public_id = db.Column(db.String(255), nullable=True)   # identificador en Cloudinary

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    # Convierte el carrusel en un diccionario para serialización de JSON
    def to_dict(self):
        return {
            "id_carrusel": self.id_carrusel,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "url_imagen": self.url_imagen,
            "public_id": self.public_id,
            "fecha_creacion": None if not self.fecha_creacion else self.fecha_creacion.isoformat()
        }

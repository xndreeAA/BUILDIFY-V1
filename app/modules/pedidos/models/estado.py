from app import db

class Estado(db.Model):
    __tablename__ = 'estados'

    id_estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(100), unique=True, nullable=False)

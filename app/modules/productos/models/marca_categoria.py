from app import db

class MarcaCategoria(db.Model):
    __tablename__ = 'marcas_categorias'
    
    id_marca_categoria = db.Column(db.Integer, primary_key=True)
    id_marca = db.Column(db.Integer, db.ForeignKey('marcas.id_marca'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    
    def __repr__(self):
        return f'<MarcaCategoria marca={self.id_marca} categoria={self.id_categoria}>'
    
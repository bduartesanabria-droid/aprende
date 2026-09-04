from app import db

Categorias =['Perros','Gatos','Vacas','Caballos','Aves','Peces']

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'
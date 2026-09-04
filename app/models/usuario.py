from flask_login import UserMixin
from app import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='admin')

    def __repr__(self):
        return f'<Admin {self.username}>'

class cliente(UserMixin, db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='cliente')

    def __repr__(self):
        return f'<Cliente {self.username}>'
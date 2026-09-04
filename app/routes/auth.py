from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models.usuario import Admin, cliente


auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    if not username or not password:
        return jsonify(error="Usuario y contrasena son obligatorios"), 400
    if cliente.query.filter_by(username=username).first():
        return jsonify(error="El usuario ya existe"), 409

    user = cliente(
        username=username,
        password=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(id=user.id, username=user.username, rol=user.rol), 201


@auth.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

    user = Admin.query.filter_by(username=username).first()
    user_type = "admin"
    if user is None:
        user = cliente.query.filter_by(username=username).first()
        user_type = "cliente"

    if user is None or not check_password_hash(user.password, password):
        return jsonify(error="Credenciales invalidas"), 401

    session["user_id"] = user.id
    session["user_type"] = user_type
    return jsonify(id=user.id, username=user.username, rol=user.rol)


@auth.post("/logout")
def logout():
    session.clear()
    return jsonify(message="Sesion cerrada")


@auth.get("/me")
def current_user():
    if "user_id" not in session:
        return jsonify(error="No autenticado"), 401

    model = Admin if session["user_type"] == "admin" else cliente
    user = db.session.get(model, session["user_id"])
    if user is None:
        session.clear()
        return jsonify(error="Usuario no encontrado"), 401

    return jsonify(id=user.id, username=user.username, rol=user.rol)

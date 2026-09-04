from flask import Blueprint, jsonify


main = Blueprint("main", __name__)


@main.get("/")
def home():
    return "Página principal"


@main.get("/health")
def health():
    return jsonify(status="ok")

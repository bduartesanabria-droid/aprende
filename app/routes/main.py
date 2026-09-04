from flask import Blueprint, jsonify, render_template
from flask import Blueprint, jsonify


main = Blueprint("main", __name__)


@main.get("/")
def home():
    return render_template(
        "index.html",
        productos=[],
        categorias=["Perros", "Gatos", "Vacas", "Caballos", "Aves", "Peces"],
    )
    return "Página principal"


@main.get("/health")
def health():
    return jsonify(status="ok")

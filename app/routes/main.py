from flask import Blueprint, jsonify, render_template


main = Blueprint("main", __name__)


@main.get("/")
def home():
    return render_template(
        "index.html",
        productos=[],
        categorias=["Perros", "Gatos", "Vacas", "Caballos", "Aves", "Peces"],
    )


@main.get("/health")
def health():
    return jsonify(status="ok")

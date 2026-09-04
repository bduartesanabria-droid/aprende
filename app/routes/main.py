from flask import Blueprint, jsonify, render_template


main = Blueprint("main", __name__)


@main.get("/")
def home():
    return render_template("index.html")


@main.get("/health")
def health():
    return jsonify(status="ok")

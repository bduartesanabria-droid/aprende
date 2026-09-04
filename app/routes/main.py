from flask import Blueprint, jsonify
from flask import flash, redirect, render_template, request, url_for

from app import db
from app.models.producto import Categorias, Producto

main = Blueprint("main", __name__)


@main.get("/")
def home():
    productos = Producto.query.order_by(Producto.id).all()
    return render_template(
        "index.html",
        productos=productos,
        categorias=Categorias,
    )


@main.route("/vendedor", methods=["GET", "POST"])
def seller():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "")
        precio_texto = request.form.get("precio", "").strip()

        try:
            precio = float(precio_texto)
        except ValueError:
            precio = -1

        if not nombre or not descripcion or categoria not in Categorias or precio < 0:
            flash("DATOS INVALIDOS // REVISA EL FORMULARIO", "error")
        else:
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                categoria=categoria,
                precio=precio,
            )
            db.session.add(producto)
            db.session.commit()
            flash("PRODUCTO REGISTRADO // CARGA COMPLETADA", "success")
            return redirect(url_for("main.seller"))

    productos = Producto.query.order_by(Producto.id.desc()).all()
    return render_template("vendedor.html", productos=productos, categorias=Categorias)


@main.get("/health")
def health():
    return jsonify(status="ok")

from flask import Blueprint, jsonify, request

from app import db
from app.models.producto import Categorias, Producto


products = Blueprint("products", __name__, url_prefix="/api/productos")


def serialize_product(product):
    return {
        "id": product.id,
        "nombre": product.nombre,
        "descripcion": product.descripcion,
        "precio": product.precio,
        "categoria": product.categoria,
    }


@products.get("")
def list_products():
    products_list = Producto.query.order_by(Producto.id).all()
    return jsonify([serialize_product(product) for product in products_list])


@products.post("")
def create_product():
    data = request.get_json(silent=True) or {}
    required = ("nombre", "descripcion", "precio", "categoria")
    missing = [field for field in required if not data.get(field)]

    if missing:
        return jsonify(error="Faltan campos", campos=missing), 400
    if data["categoria"] not in Categorias:
        return jsonify(error="Categoria no valida", categorias=Categorias), 400

    try:
        price = float(data["precio"])
    except (TypeError, ValueError):
        return jsonify(error="El precio debe ser numerico"), 400

    if price < 0:
        return jsonify(error="El precio no puede ser negativo"), 400

    product = Producto(
        nombre=str(data["nombre"]).strip(),
        descripcion=str(data["descripcion"]).strip(),
        precio=price,
        categoria=data["categoria"],
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(serialize_product(product)), 201


@products.get("/<int:product_id>")
def get_product(product_id):
    product = db.session.get(Producto, product_id)
    if product is None:
        return jsonify(error="Producto no encontrado"), 404
    return jsonify(serialize_product(product))


@products.put("/<int:product_id>")
def update_product(product_id):
    product = db.session.get(Producto, product_id)
    if product is None:
        return jsonify(error="Producto no encontrado"), 404

    data = request.get_json(silent=True) or {}
    for field in ("nombre", "descripcion"):
        if field in data:
            setattr(product, field, str(data[field]).strip())

    if "categoria" in data:
        if data["categoria"] not in Categorias:
            return jsonify(error="Categoria no valida", categorias=Categorias), 400
        product.categoria = data["categoria"]

    if "precio" in data:
        try:
            price = float(data["precio"])
        except (TypeError, ValueError):
            return jsonify(error="El precio debe ser numerico"), 400
        if price < 0:
            return jsonify(error="El precio no puede ser negativo"), 400
        product.precio = price

    db.session.commit()
    return jsonify(serialize_product(product))


@products.delete("/<int:product_id>")
def delete_product(product_id):
    product = db.session.get(Producto, product_id)
    if product is None:
        return jsonify(error="Producto no encontrado"), 404

    db.session.delete(product)
    db.session.commit()
    return "", 204

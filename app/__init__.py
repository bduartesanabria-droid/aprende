from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="dev-secret-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    from app.routes import auth, main, products

    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(auth)

    with app.app_context():
        from app.models import producto, usuario  # noqa: F401

        db.create_all()

    return app

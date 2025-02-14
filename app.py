import os

from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from db import db


from resources.chemical import blp as ChemicalBlueprint
from resources.reaction import blp as ReactionBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    CORS(app)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)


    with app.app_context():
        db.create_all()

    api.register_blueprint(ChemicalBlueprint)
    api.register_blueprint(ReactionBlueprint)

    return app
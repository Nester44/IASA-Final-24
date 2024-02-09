from flask import Flask
from flask_restful import Api
from config import Config
from .api.routes import initialize_routes
from flask_cors import CORS


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app)
    CORS(app)

    initialize_routes(api)

    return app

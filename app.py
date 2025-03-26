import os

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

import logging
from logging.handlers import RotatingFileHandler

from db import db
import models   # noqa

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


def create_logger():
    logging_handler = RotatingFileHandler(
        'logs/app.log', maxBytes=10000, backupCount=5)
    logging_handler.setLevel(logging.INFO)

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)
    logging_handler.setFormatter(formatter)

    return logging_handler


def create_app(db_url=None):
    app = Flask(__name__)

    logging_handler = create_logger()
    app.logger.addHandler(logging_handler)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'Store API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/' # noqa
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)

    app.config['JWT_SECRET'] == os.getenv('JWT_SECRET')
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    app.logger.info('App created successfully.')

    return app

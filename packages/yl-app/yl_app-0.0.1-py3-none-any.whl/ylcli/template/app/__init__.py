from app.api.v1 import create_blueprint_v1
from .app import Flask


def create_app():
    _app = Flask(__name__)
    _app.config.from_object('app.config.secure')
    _app.config.from_object('app.config.setting')
    register_blueprints(_app)
    # register_plugin(_app)
    return _app


def register_blueprints(_app):
    from app.api.v1 import create_blueprint_v1
    _app.register_blueprint(create_blueprint_v1(), url_prefix="/yl")


def register_plugin(_app):
    from app.models.base import db
    db.init_app(_app)
    with _app.app_context():
        db.create_all()

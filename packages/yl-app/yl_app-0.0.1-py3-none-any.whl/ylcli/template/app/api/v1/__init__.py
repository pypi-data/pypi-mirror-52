from flask import Blueprint
from app.api.v1 import Greeting
from flask_cors import CORS

api_collect = [Greeting]


def create_blueprint_v1():
    bp_v1 = Blueprint("yl", __name__)
    register(api_collect, bp_v1, 'v1')
    CORS(bp_v1)
    return bp_v1


def register(modules, bp, version):
    for module in modules:
        for api in getattr(module, version, []):
            api.register(bp)

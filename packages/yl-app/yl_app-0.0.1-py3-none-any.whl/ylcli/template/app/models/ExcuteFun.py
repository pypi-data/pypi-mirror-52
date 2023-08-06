from flask.json import jsonify

from app.libs.util import refine_args
from app.models.base import db


class BaseExcute:
    def __init__(self, sql):
        self.sql = sql

    @refine_args
    def go(self, **json):
        self.sql = self.sql.format(**json['params'])
        res = db.session.execute(self.sql)
        result = res.fetchone()
        msg = {}
        for item in result.items():
            msg[item[0]] = item[1]
        return jsonify(msg)

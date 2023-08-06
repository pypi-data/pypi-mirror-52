from app.libs.error_code import Success
from app.libs.util import refine_args
from app.models.base import db


class BaseOperate:
    def __init__(self, cls):
        self.tab = cls

    @refine_args
    def go(self, **json):
        if json['method'] == 'GET':
            return self.get(self.tab, **json)

        elif json['method'] == 'PUT':
            return self.put(self.tab, **json)

        elif json['method'] == 'POST':
            return self.post(self.tab, **json)
        else:
            return self.delete(self.tab, **json)

    @staticmethod
    def get(cls, **json):
        return cls.auto_query(**json['params'])

    @staticmethod
    def put(cls, **json):
        with db.auto_commit():
            item = cls.query.get(json['params']['ID'])
            item.set_attrs(json['params'])
        return Success()

    @staticmethod
    def post(cls, **json):
        with db.auto_commit():
            item = cls()
            item.set_attrs(json['params'])
            db.session.add(item)
        return Success()

    @staticmethod
    def delete(cls, **json):
        with db.auto_commit():
            item = cls.query.get(json['params']['ID'])
            db.session.delete(item)
        return Success()


class BatchPost:
    def __init__(self, cls):
        self.tab = cls

    @refine_args
    def go(self, **json):
        params = json['params']
        with db.auto_commit():
            for item in params:
                instance = self.tab()
                instance.set_attrs(item)
                db.session.add(instance)
        return Success()


class BatchPut:
    def __init__(self, cls):
        self.tab = cls

    @refine_args
    def go(self, **json):
        params = json['params']
        with db.auto_commit():
            for item in params:
                temp = self.tab.query.get(item['ID'])
                temp.set_attrs(item)
        return Success()

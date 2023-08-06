from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from contextlib import contextmanager
from app.libs.error_code import NotFound, ServerError
from app.libs.util import query_db


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):

    # 软删除
    # def filter_by(self, **kwargs):
    #     if 'status' not in kwargs.keys():
    #         kwargs['status'] = 1
    #     return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 避免创建Base表
    __abstract__ = True

    # 序列化时使用dict方法会调用该方法
    def __getitem__(self, item):
        return getattr(self, item)

    def set_attrs(self, attrs_dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k != "ID":
                setattr(self, k, v)

    # auto_query
    @classmethod
    def auto_query(cls, **json):
        binds = getattr(cls, '__bind_key__') if hasattr(cls, '__bind_key__') else None
        engine = db.get_engine(bind=binds)
        return query_db(cls, engine=engine, view=False, **json)

    @staticmethod
    def keys():
        pass

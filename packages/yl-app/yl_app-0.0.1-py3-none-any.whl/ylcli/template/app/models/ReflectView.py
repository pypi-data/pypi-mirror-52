from app.libs.util import query_db, refine_args
from app.models.base import db


class MyView:
    def __init__(self, tab_name, bind=None):
        self.engine = db.get_engine(bind=bind)
        db.metadata.reflect(bind=self.engine, views=True)
        self.view = db.metadata.tables[tab_name]

    @refine_args
    def query(self, **json):
        return query_db(self.view, self.engine, view=True, **json['params'])

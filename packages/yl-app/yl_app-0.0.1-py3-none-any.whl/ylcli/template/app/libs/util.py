import re
from functools import wraps
from flask import request, current_app, Response
from flask.json import jsonify
from sqlalchemy import desc, asc, String, VARCHAR as _VARCHAR, CHAR as _CHAR
from sqlalchemy.dialects.mysql import VARCHAR, CHAR
from sqlalchemy.orm import sessionmaker
from app.app import JSONEncoder


def refine_args(fun):
    @wraps(fun)
    def wrapper(self=None, *args, **kwargs):
        params = request.get_json(silent=True) or (request.args.to_dict() if request.args else {})
        json = {
            'params': params,
            'method': request.method
        }
        res = fun(self, **json)
        if isinstance(res, Response):
            res.headers['Access-Control-Expose-Headers'] = 'Date'
        return res

    return wrapper


def json_to_firters(model, **json):
    filters = ()
    for k, v in json.items():
        reg = re.search('^([a-zA-Z-_]+?)(!|>|<|>=|<=)$', k)
        if reg:
            key = reg.groups()[0]
            flag = reg.groups()[1]
        else:
            flag = None
            key = k
        if key.lower() not in ['skip', 'take', 'orderby']:
            filters += append_filter(model, flag, key, v)

    if not json.__contains__("skip"):
        skip = 0
    elif isinstance(json['skip'], int):
        skip = json['skip']
    elif isinstance(json['skip'], str) and re.match('[0-9]+', json['skip']):
        skip = int(json["skip"])
    else:
        skip = 0

    if not json.__contains__("take"):
        take = current_app.config["LIMIT"]
    elif isinstance(json['take'], int):
        take = json['take']
    elif isinstance(json['take'], str) and re.match('[0-9]+', json['take']):
        take = int(json["take"])
    else:
        take = current_app.config["LIMIT"]

    orderby = json['orderby'] if json.__contains__('orderby') else None
    return {
        'filters': filters,
        'skip': skip,
        'take': take,
        'orderby': orderby
    }


def append_filter(model, flag, k, v):
    # 字符串
    if isinstance(getattr(model, k).type, (VARCHAR, CHAR, String, _VARCHAR, _CHAR)):
        if flag == '!':
            temp_tuple = getattr(model, k) != v,
        else:
            temp_tuple = getattr(model, k).like("%" + v + "%"),
        return temp_tuple
    # 数值(暂不考虑日期类型)
    else:
        v = float(v)
        if flag == '!':
            temp_tuple = getattr(model, k) != v,
        elif flag == '>':
            temp_tuple = getattr(model, k) > v,
        elif flag == '<':
            temp_tuple = getattr(model, k) < v,
        elif flag == '>=':
            temp_tuple = getattr(model, k) >= v,
        elif flag == '<=':
            temp_tuple = getattr(model, k) <= v,
        else:
            temp_tuple = getattr(model, k) == v,
        return temp_tuple


def query_db(cls, engine=None, view=False, **json):
    # 基表会绑定 _bind_key_ 故而不需要
    Session = sessionmaker(bind=engine)
    session = Session()
    params = json_to_firters(cls.c if view else cls, **json)
    reg = False if not params['orderby'] else \
        re.search('^(-?)([a-zA-Z-_]+?)$', params['orderby'])
    orderby = reg.groups()[1] if reg else False
    if reg and orderby and hasattr(cls.c if view else cls, orderby):
        order_meth = desc if reg.groups()[0] else asc
        res = session.query(cls).order_by( \
            order_meth(getattr(cls.c if view else cls, orderby))). \
            filter(*params['filters']).offset(params['skip']).limit(params['take'])
    else:
        res = session.query(cls).filter(*params['filters']) \
            .offset(params['skip']).limit(params['take'])
    Results = [item._asdict() for item in res] if view else res.all()
    Total = res.count()
    # 主动关闭会话 释放数据库连接
    session.close()
    return jsonify({
        'Results': Results,
        'Total': Total
    })

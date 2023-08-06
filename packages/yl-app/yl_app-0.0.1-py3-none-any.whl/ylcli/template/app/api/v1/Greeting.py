from flask.json import jsonify

from app.libs.redPrint import RedPrint

api = RedPrint('greeting')

v1 = [api]


@api.route('', methods=['GET'])
def greeting():
    res = {
        'msg': 'Welcome!',
        'errorCode': 0
    }
    return jsonify(res)

from flask import request, json

from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = "sorry, we make a mistake (๑•̀ㅂ•́)و✧"
    error_code = 999
    headers = {
        'Access-Control-Expose-Headers': 'Date'
    }

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if headers:
            self.headers = headers
        super(APIException, self).__init__(msg, None)

    # 将默认返回html的行为更改为返回json字符串
    def get_body(self, environ=None):
        body = dict(msg=self.msg,
                    errCode=self.error_code,
                    request=request.method + " " + self.get_url_no_param()
                    )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        cur_headers = super(APIException, self).get_headers()
        for k, v in self.headers.items():
            cur_headers.append((k, v))
        return cur_headers

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        return full_path.split("?")[0]

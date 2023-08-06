from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()


# 整体错误处理
@app.errorhandler(Exception)
def framework_error(Exception):
    if isinstance(Exception, APIException):
        return Exception
    elif isinstance(Exception, HTTPException):
        code = Exception.code
        msg = Exception.description
        error_code = 1007
        return APIException(code=code, msg=msg, error_code=error_code)
    else:
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise Exception


if __name__ == '__main__':
    app.run(port=app.config['PORT'], \
            debug=app.config['DEBUG'], host=app.config['HOST'], threaded=True)

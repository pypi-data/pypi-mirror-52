from app.libs.error import APIException


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 0


class InsertSuccess(Success):
    code = 203
    error_code = 0


class ServerError(APIException):
    code = 500
    msg = "sorry we make a mistake (๑•̀ㅂ•́)و✧"
    error_code = 999


class ClientTypeException(APIException):
    code = 400
    error_code = 1006
    msg = "client is invalid"


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not_found ヽ(✿ﾟ▽ﾟ)ノ'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'

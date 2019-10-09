# @Time    : 2019-08-01 18:26
# @Author  : 白尚林
# @File    : resp
# @Use     :

from .exception import APIException


class Success(APIException):
    code = 200
    msg = 'ok!'
    errno = 0


class GetSuccess(Success):
    pass


class PostSuccess(Success):
    code = 201


class PutSuccess(Success):
    pass


class PatchSuccess(Success):
    pass


class DeleteSuccess(Success):
    code = 204

class PartialSuccess(Success):
    code = 206

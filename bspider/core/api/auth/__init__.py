# @Time    : 2019/6/20 1:28 PM
# @Author  : 白尚林
# @File    : __init__.py
# @Use     :
from flask import g
from flask_httpauth import HTTPTokenAuth
from .token import verify_token

auth = HTTPTokenAuth()


@auth.verify_token
def verify_ctx_token(x_token: str) -> bool:
    user = verify_token(x_token)
    if user:
        g.user = user
        return True
    return False

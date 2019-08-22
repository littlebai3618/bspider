# @Time    : 2019-08-01 16:32
# @Author  : 白尚林
# @File    : token
# @Use     :
from collections import namedtuple

import casbin
from flask import current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

from core.api.auth import MySQLAdapter
from core.api.exception import AuthFailed, Forbidden
from util.path import ROOT_PATH
from util.logger.log_handler import LoggerPool

__log = LoggerPool().get_logger('api_auth', module='api_auth')

User = namedtuple('User', ['user_id', 'role'])
e = casbin.Enforcer(f'{ROOT_PATH}/core/api/auth/rbac_model.conf', adapter=MySQLAdapter())


def make_token(user_id, role):
    s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=7200)
    return s.dumps({'user_id': user_id, 'role': role}).decode('ascii')


def verify_token(token):
    s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', errno=10002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', errno=10003)
    if e.enforce(data['role'], request.method, request.endpoint):
        __log.info('user:{}-{} request:{} pass verify'.format(data['user_id'], data['role'], request.endpoint))
        return User(data['user_id'], data['role'])
    __log.info('user:{}-{} request:{} auth failed'.format(data['user_id'], data['role'], request.endpoint))
    raise Forbidden(code=403, msg='forbidden, op failed')

import os
from collections import namedtuple

import casbin
from flask import request
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired

import bspider
from bspider.config import FrameSettings
from bspider.core.api.exception import AuthFailed, Forbidden
from bspider.utils.logger import LoggerPool

__log = LoggerPool().get_logger(key='api_auth', fn='auth', module='api_auth')
__key = FrameSettings()['WEB_SECRET_KEY']

User = namedtuple('User', ['user_id', 'role', 'token'])
e = casbin.Enforcer(os.path.join(bspider.__path__[0], 'config', 'rbac_model.conf'),
                    os.path.join(bspider.__path__[0], 'config', 'rbac_policy.csv'))


def make_token(user_id, role):
    s = TimedJSONWebSignatureSerializer(__key, expires_in=7200)
    return s.dumps({'user_id': user_id, 'role': role}).decode('ascii')


def verify_token(token):
    s = TimedJSONWebSignatureSerializer(__key)
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', errno=10002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', errno=10003)
    if e.enforce(data['role'], request.method.upper(), request.blueprint):
        __log.info(
            'user:{}-{} request:{} {} pass verify'.format(data['user_id'], data['role'], request.endpoint, request.method))
        return User(data['user_id'], data['role'], token)
    __log.info(
        'user:{}-{} request:{} {} auth failed'.format(data['user_id'], data['role'], request.endpoint, request.method))
    raise Forbidden(msg='Unauthorized operation', errno=10004)

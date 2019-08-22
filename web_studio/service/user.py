# @Time    : 2019/6/19 1:54 PM
# @Author  : 白尚林
# @File    : user
# @Use     :
from pymysql import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from core.api import BaseService
from core.api.auth.token import make_token
from core.api.exception import ParameterException, NotFound, PreconditionFailed, Conflict
from core.api.resp import GetSuccess, PostSuccess, DeleteSuccess, PatchSuccess
from web_studio.server import log
from web_studio.service.impl import UserImpl

class UserService(BaseService):

    def __init__(self):
        self.impl = UserImpl()

    def login(self, identity, password):
        info = self.impl.get_user(identity)
        if len(info) == 1:
            info = info[0]
            if check_password_hash(info.pop('password'), password):
                info['token'] = make_token(info['id'], info['role'])
                info.pop('identity')
                log.info(f'user:{identity} login success')
                return GetSuccess(msg='login success', data=info)
            else:
                log.info(f'user:{identity} login failed:invalid password')
                return ParameterException(errno=10005, msg='invalid password')
        elif len(info) == 0:
            log.info(f'user:{identity} login failed:invalid user')
            return NotFound(errno=10006, msg='invalid user')

    def add_user(self, identity, username, password, role, email, phone):
        data = {
            'identity': identity,
            'username': username,
            'password': generate_password_hash(password),
            'role': role,
            'email': email,
            'phone': phone
        }
        try:
            user_id = self.impl.add_user(data)
            data['user_id'] = user_id
            data.pop('password')
            log.info(f'user:{identity} add success')
            return PostSuccess(msg=f'add user {username} success', data=data)
        except IntegrityError as e:
            if e.args[0] == 1062:
                log.info(f'user:{identity} add failed:user is already exist')
                return Conflict(errno=10007, msg='user is already exist')
            raise e

    def remove_user(self, user_id):
        self.impl.remove_user(user_id)
        log.warning(f'user:{user_id} delete success')
        return DeleteSuccess()

    def update_user(self, user_id, **kwargs):
        update_info = {}
        for key, value in kwargs.items():
            if value is None:
                continue
            if 'password' == key:
                value = generate_password_hash(value)
            update_info[key] = value
        self.impl.update_user(user_id, **update_info)
        log.info(f'user:{user_id} update success with:{update_info}')
        return PatchSuccess(msg='update user success!')

    def get_users(self):
        infos = self.impl.get_users()
        for info in infos:
            info.pop('password')
        return GetSuccess(msg='get user list success!', data=infos)

    def get_user(self, user_id):
        info = self.impl.get_user_by_id(user_id)
        if len(info):
            return GetSuccess(msg='get user success', data=info[0])
        return NotFound(errno=10006, msg='invalid user')

from pymysql import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from bspider.core.api import BaseService, ParameterException, NotFound, Conflict, GetSuccess, PostSuccess, DeleteSuccess, PatchSuccess
from bspider.core.api.auth.token import make_token

from bspider.master.server import log
from bspider.master.service.impl.user_impl import UserImpl


class UserService(BaseService):

    def __init__(self):
        self.impl = UserImpl()

    def login_by_identity(self, identity, password):
        infos = self.impl.get_user(identity)

        for info in infos:
            self.datetime_to_str(info)

        if len(infos) == 1:
            info = infos[0]
            if info['status'] == 0:
                return Conflict(errno=10009, msg='this identity was closed, please call admin!')

            if check_password_hash(info.pop('password'), password):
                info['token'] = make_token(info['id'], info['role'])
                log.info(f'user->identity:{identity} login success')
                return GetSuccess(msg='login success', data=info)
            else:
                log.info(f'user->identity:{identity} login failed:invalid password')
                return ParameterException(errno=10005, msg='invalid password')
        elif len(infos) == 0:
            log.info(f'user->identity:{identity} login failed:invalid user')
            return NotFound(errno=10006, msg='invalid user')
        else:
            return Conflict(errno=10008, msg='query exceptions')

    def add_user(self, identity, username, password, role, email, phone, status):
        data = {
            'identity': identity,
            'username': username,
            'password': generate_password_hash(password),
            'role': role,
            'email': email,
            'phone': phone,
            'status': status
        }
        try:
            user_id = self.impl.add_user(data)
            data['user_id'] = user_id
            data.pop('password')
            log.info(f'user->identity:{identity} add success')
            return PostSuccess(msg=f'add user {username} success', data=data)
        except IntegrityError as e:
            if e.args[0] == 1062:
                log.info(f'user->identity:{identity} add failed:user is already exist')
                return Conflict(errno=10007, msg='user is already exist')
            raise e

    def remove_user(self, user_id):
        self.impl.remove_user(user_id)
        log.warning(f'user->user_id:{user_id} delete success')
        return DeleteSuccess()

    def update_user(self, user_id, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = generate_password_hash(kwargs['password'])
        self.impl.update_user(user_id, kwargs)
        log.info(f'user->user_id:{user_id}->{kwargs} update success')
        return PatchSuccess(msg='update user success!')

    def get_users(self, page, limit, search, sort):
        if sort.upper() not in ['ASC', 'DESC']:
            return ParameterException(msg='sort must `asc` or `desc`')

        infos, total = self.impl.get_users(page, limit, search, sort)

        for info in infos:
            info.pop('password')
            self.datetime_to_str(info)

        return GetSuccess(
            msg='get user list success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })

    def get_user(self, user_id):
        infos = self.impl.get_user_by_id(user_id)

        for info in infos:
            self.datetime_to_str(info)

        if len(infos):
            return GetSuccess(msg='get user success', data=infos[0])
        return NotFound(errno=10006, msg='invalid user')

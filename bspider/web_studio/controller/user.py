# @Time    : 2019/6/19 2:17 PM
# @Author  : 白尚林
# @File    : user
# @Use     :
from flask import Blueprint, g

from bspider.core.api import auth
from bspider.core.api import NotFound
from .validators.user_forms import LoginForm, RegisterForm, UpdateForm
from bspider.web_studio.service.user import UserService

user = Blueprint('user_bp', __name__)

user_service = UserService()


@user.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    client = form.client_type.data
    if client == 'identity':
        return user_service.login(form.identity.data, form.password.data)
    else:
        return NotFound(msg='unknow client type')


@user.route('/user', methods=['POST'])
@auth.login_required
def add_user():
    form = RegisterForm()
    return user_service.add_user(form.identity.data, form.username.data, form.password.data,
                                 form.role.data, form.email.data, form.phone.data)


@user.route('/user/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    return user_service.remove_user(user_id)


@user.route('/user/<int:user_id>', methods=['PATCH'])
@auth.login_required
def update_user(user_id):
    form = UpdateForm()
    data = {
        'username': form.username.data,
        'password': form.password.data,
        'phone': form.phone.data,
        'email': form.email.data,
        'role': form.role.data
    }
    return user_service.update_user(user_id, **data)


@user.route('/user', methods=['GET'])
@auth.login_required
def get_users():
    return user_service.get_users()


@user.route('/user/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    return user_service.get_user(user_id)

@user.route('/current_user', methods=['GET'])
@auth.login_required
def get_current_user():
    return user_service.get_user(g.user.user_id)

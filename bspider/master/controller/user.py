from flask import Blueprint

from bspider.core.api import auth
from bspider.core.api import NotFound
from .validators import PageForm
from .validators.user_forms import LoginForm, RegisterForm, UpdateForm
from bspider.master.service.user import UserService

user = Blueprint('user_bp', __name__)

user_service = UserService()


@user.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    client = form.client_type.data
    if client == 'identity':
        return user_service.login_by_identity(form.identity.data, form.password.data)
    else:
        return NotFound(msg='unknow client type')


@user.route('/user', methods=['POST'])
@auth.login_required
def add_user():
    form = RegisterForm()
    return user_service.add_user(**form.to_dict())


@user.route('/user/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    return user_service.remove_user(user_id)


@user.route('/user/<int:user_id>', methods=['PATCH'])
@auth.login_required
def update_user(user_id):
    form = UpdateForm()
    return user_service.update_user(user_id, **form.to_dict())


@user.route('/user', methods=['GET'])
@auth.login_required
def get_users():
    form = PageForm()
    return user_service.get_users(int(form.page.data), int(form.limit.data), form.search.data, form.sort.data)


@user.route('/user/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    return user_service.get_user(user_id)

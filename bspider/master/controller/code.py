from flask import Blueprint, g

from bspider.core.api import auth, Forbidden
from bspider.master.service.code import CodeService
from .validators.code_forms import AddForm, UpdateForm
from .validators import PageForm

code = Blueprint('code_bp', __name__)

code_service = CodeService()


@code.route('/code/<int:code_id>', methods=['GET'])
@auth.login_required
def get(code_id):
    return code_service.get_code(code_id)


@code.route('/code', methods=['GET'])
@auth.login_required
def gets():
    form = PageForm()
    return code_service.get_codes(**form.to_dict())


@code.route('/code', methods=['POST'])
@auth.login_required
def add():
    form = AddForm()
    # 非admin角色不能新增operation 类
    if form.name.data.lower().rfind('operation') != -1 and g.user.role != 'admin':
        raise Forbidden(msg='role has no permission!', errno=10004)
    return code_service.add(**form.to_dict())


@code.route('/code/<int:code_id>', methods=['DELETE'])
@auth.login_required
def delete(code_id):
    return code_service.delete(code_id)


@code.route('/code/<int:code_id>', methods=['PATCH'])
@auth.login_required
def update(code_id):
    form = UpdateForm()
    # 非admin角色不能修改operation 类
    if form.name.data.lower().rfind('operation') != -1 and g.user.role != 'admin':
        raise Forbidden(msg='role has no permission!', errno=10004)
    return code_service.update(code_id, **form.to_dict())

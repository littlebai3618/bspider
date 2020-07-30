"""
    封装对cache中code信息的操作为api
"""
from flask import Blueprint

from bspider.core.api import auth
from .validators.code_form import AddForm, UpdateForm
from bspider.agent.service.code import CodeService

code = Blueprint('code_bp', __name__)
code_service = CodeService()


@code.route('/code', methods=['POST'])
@auth.login_required
def add_code():
    form = AddForm()
    return code_service.add_code(**form.to_dict())


@code.route('/code/<int:code_id>', methods=['PATCH'])
@auth.login_required
def update_code(code_id):
    form = UpdateForm()
    return code_service.update_code(code_id, form.to_dict())


@code.route('/code/<int:code_id>', methods=['DELETE'])
@auth.login_required
def delete_code(code_id):
    return code_service.delete_code(code_id)


@code.route('/code', methods=['GET'])
@auth.login_required
def get_codes():
    return code_service.get_codes()


@code.route('/code/<int:code_id>', methods=['GET'])
def get_code(code_id):
    return code_service.get_code(code_id)

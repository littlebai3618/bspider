# @Time    : 2019/6/23 12:52 PM
# @Author  : 白尚林
# @File    : code
# @Use     :
from flask import Blueprint

from web_studio.controller.validators.code_forms import GetForm, AddForm, UpdateForm
from web_studio.service.code import CodeService

code = Blueprint('code_bp', __name__)

code_service = CodeService()

@code.route('/code/<int:code_id>', methods=['GET'])
# @Auth
def get(code_id):
    return code_service.get_code(code_id)

@code.route('/code', methods=['GET'])
# @Auth
def gets():
    form = GetForm()
    param = form.get_dict()
    print(param)
    if form.code_type.data:
        return code_service.get_codes(**param)
    return code_service.get_codes()

@code.route('/code', methods=['POST'])
# @Auth
def add():
    form = AddForm()
    return code_service.add(form.name.data, form.description.data, form.type.data, form.content.data, form.editor.data)

@code.route('/code/<int:code_id>', methods=['DELETE'])
# @Auth
def delete(code_id):
    return code_service.delete(code_id)

@code.route('/code', methods=['PATCH'])
# @Auth
def update():
    form = UpdateForm()
    changes = form.get_dict()
    code_id = changes.pop('code_id')
    code_name = changes.pop('name')
    return code_service.update(code_id, code_name, changes)

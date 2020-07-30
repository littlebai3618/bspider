from flask import Blueprint

from bspider.core.api import auth
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
    return code_service.add(**form.to_dict())


@code.route('/code/<int:code_id>', methods=['DELETE'])
@auth.login_required
def delete(code_id):
    return code_service.delete(code_id)


@code.route('/code/<int:code_id>', methods=['PATCH'])
@auth.login_required
def update(code_id):
    form = UpdateForm()
    return code_service.update(code_id, **form.to_dict())

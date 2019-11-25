# @Time    : 2019/7/12 11:25 AM
# @Author  : 白尚林
# @File    : tools
# @Use     :
"""
1. 获取node ip列表 /tools/nodelist [{name: , ip:}]
"""
from flask import Blueprint

from bspider.core.api import auth
from bspider.master.service.tools import ToolsService

from .validators.tools_forms import GetCodeListForm, ValidateForm


tools = Blueprint('tools_bp', __name__)

tools_service = ToolsService()


@tools.route('/nodelist', methods=['GET'])
@auth.login_required
def node_list():
    """返回节点列表"""
    return tools_service.get_node_list()

@tools.route('/codelist', methods=['GET'])
@auth.login_required
def code_list():
    """返回节点列表"""
    form = GetCodeListForm()
    return tools_service.get_code_list(form.type.data)

@tools.route('/validate/<string:valid_type>', methods=['GET'])
@auth.login_required
def validate(valid_type):
    """返回节点列表"""
    form = ValidateForm()
    return tools_service.validate(valid_type, form.data.data)

@tools.route('/parser/exception/<int:project_id>', methods=['GET'])
@auth.login_required
def parser_exception(project_id):
    """返回节点列表"""
    return tools_service.get_parser_exception(project_id)

@tools.route('/downloader/exception/<int:project_id>', methods=['GET'])
@auth.login_required
def downloader_exception(project_id):
    """返回节点列表"""
    return tools_service.get_downloader_exception(project_id)


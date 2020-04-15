from flask import Blueprint, g

from bspider.core.api import auth
from bspider.master.service.tools import ToolsService

from .validators.tools_forms import GetCodeListForm, ValidateForm, GetCrawlDetailForm

tools = Blueprint('tools_bp', __name__)

tools_service = ToolsService()


@tools.route('/node-list', methods=['GET'])
@auth.login_required
def node_list():
    """返回节点列表"""
    return tools_service.get_node_list()


@tools.route('/code-list', methods=['GET'])
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


@tools.route('/crawl-detail', methods=['GET'])
@auth.login_required
def crawl_detail():
    """返回节点列表"""
    form = GetCrawlDetailForm()
    return tools_service.get_crawl_detail(**form.to_dict())


@tools.route('/node-detail', methods=['GET'])
@auth.login_required
def node_detail():
    """返回节点列表"""
    return tools_service.get_node_detail()


@tools.route('/exception-project', methods=['GET'])
@auth.login_required
def exception_project():
    """返回节点列表"""
    return tools_service.get_exception_project()

@tools.route('/current_user', methods=['GET'])
@auth.login_required
def get_current_user():
    return tools_service.get_current_user(g.user.user_id)

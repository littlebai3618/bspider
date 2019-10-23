# @Time    : 2019/7/12 11:25 AM
# @Author  : 白尚林
# @File    : tools
# @Use     :
"""
1. 获取node ip列表 /tools/nodelist [{name: , ip:}]
"""
from flask import Blueprint

from bspider.core.api import auth
from bspider.web_studio.service.tools import ToolsService

tools = Blueprint('tools_bp', __name__)

tools_service = ToolsService()


@tools.route('/nodelist', methods=['GET'])
@auth.login_required
def node_list():
    """返回节点列表"""
    return tools_service.get_node_list()

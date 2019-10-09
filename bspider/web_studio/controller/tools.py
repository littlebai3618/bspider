# @Time    : 2019/7/12 11:25 AM
# @Author  : 白尚林
# @File    : tools
# @Use     :
"""待开发内容"""
from flask import request, Blueprint
from bspider.utils import resp
from bspider.web_studio.service import ToolsService

tools = Blueprint('tools_bp', __name__)

tools_service = ToolsService()

@tools.route('/error', methods=['POST'])
# @Auth
def error():
    """获取解析器异常"""
    project_name = request.json.get('project_name')
    error_type = request.json.get('error_type')
    if project_name and error_type:
        if error_type == 'parser':
            return resp(*tools_service.get_parser_error(project_name))
        elif error_type == 'downloader':
            return resp(*tools_service.get_downloader_error(project_name))
        else:
            resp(3, '未知的模块{}'.format(error_type))
    else:
        resp(2, '参数错误 非法的project_name 或 error_type')

@tools.route('/reqtrack', methods=['POST'])
# @Auth
def reqtrack():
    url = request.json.get('url')
    sign = request.json.get('sign')
    if url:
        return resp(*tools_service.get_reqest_track(url=url))
    elif sign:
        return resp(*tools_service.get_reqest_track(sign=sign))
    else:
        return resp(2, '参数错误无效的url 或 sign')

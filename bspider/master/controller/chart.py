# @Time    : 2019/11/22 7:49 下午
# @Author  : baii
# @File    : chart
# @Use     :
from flask import Blueprint

from bspider.core.api import auth
from bspider.master.service.chart import ChartService

chart = Blueprint('chart_bp', __name__)

chart_service = ChartService()


@chart.route('/downloader', methods=['GET'])
@auth.login_required
def downloader_pv():
    """返回节点列表"""
    return chart_service.downloader_pv()

@chart.route('/downloader/<int:project_id>', methods=['GET'])
@auth.login_required
def downloader_pv_by_project(project_id):
    """返回节点列表"""
    return chart_service.downloader_pv(project_id)

@chart.route('/parser', methods=['GET'])
@auth.login_required
def parser_pv():
    """返回节点列表"""
    return chart_service.parser_pv()

@chart.route('/parser/<int:project_id>', methods=['GET'])
@auth.login_required
def parser_pv_by_project(project_id):
    """返回节点列表"""
    return chart_service.parser_pv(project_id)

@chart.route('/code-type-detail', methods=['GET'])
@auth.login_required
def code_type_detail():
    """获取每种code的数量"""
    return chart_service.get_code_type_detail()

@chart.route('/node-detail/<str:node_ip>', methods=['GET'])
@auth.login_required
def node_pv(node_ip):
    """获取节点状态信息"""
    return chart_service.node_pv(node_ip)
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
def downloader_pv(project_id):
    """返回节点列表"""
    return chart_service.downloader_pv(project_id)

@chart.route('/parser', methods=['GET'])
@auth.login_required
def downloader_pv():
    """返回节点列表"""
    return chart_service.parser_pv()

@chart.route('/parser/<int:project_id>', methods=['GET'])
@auth.login_required
def downloader_pv(project_id):
    """返回节点列表"""
    return chart_service.parser_pv(project_id)

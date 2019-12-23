from flask import Blueprint

from bspider.core.api import auth
from bspider.master.service.chart import ChartService

chart = Blueprint('chart_bp', __name__)

chart_service = ChartService()


@chart.route('/downloader', methods=['GET'])
@auth.login_required
def downloader_pv():
    return chart_service.downloader_pv()


@chart.route('/downloader/<int:project_id>', methods=['GET'])
@auth.login_required
def downloader_pv_by_project(project_id):
    return chart_service.downloader_pv(project_id)


@chart.route('/parser', methods=['GET'])
@auth.login_required
def parser_pv():
    return chart_service.parser_pv()


@chart.route('/parser/<int:project_id>', methods=['GET'])
@auth.login_required
def parser_pv_by_project(project_id):
    return chart_service.parser_pv(project_id)


@chart.route('/code-type-detail', methods=['GET'])
@auth.login_required
def code_type_detail():
    return chart_service.get_code_type_detail()


@chart.route('/node-detail/<string:node_ip>', methods=['GET'])
@auth.login_required
def node_pv(node_ip):
    return chart_service.node_pv(node_ip)

# @Time    : 2019/11/19 2:11 下午
# @Author  : baii
# @File    : rabbitmq
# @Use     : 队列信息接口
from flask import Blueprint

from bspider.core.api import auth
from bspider.master.service.rabbitmq import RabbitMQService

rabbitmq = Blueprint('rabbitmq_bp', __name__)

rabbitmq_service = RabbitMQService()


@rabbitmq.route('/project/<int:project_id>', methods=['GET'])
@auth.login_required
def project_queue_info(project_id):
    """project相关队列的详细信息"""
    return rabbitmq_service.get_project_queue_info(project_id)

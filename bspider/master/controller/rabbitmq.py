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


@rabbitmq.route('/project/purge/<int:project_id>', methods=['DELETE'])
@auth.login_required
def purge_project_queue(project_id):
    """清空待下载链接"""
    return rabbitmq_service.purge_project_queue(project_id)

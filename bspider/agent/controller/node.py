# @Time    : 2019/7/17 2:23 PM
# @Author  : 白尚林
# @File    : node
# @Use     :
from flask import Blueprint

from bspider.agent.service.node import NodeService
from bspider.core.api import auth
from .validators.worker_forms import RegisterForm

node = Blueprint('node_bp', __name__)

node_service = NodeService()

@node.route('/node', methods=['GET'])
@auth.login_required
def status():
    return node_service.node_status()

@node.route('/worker', methods=['POST'])
@auth.login_required
def start_worker():
    form = RegisterForm()
    return node_service.start_worker(**form.get_dict())

@node.route('/worker/<int:worker_id>', methods=['DELETE'])
@auth.login_required
def stop_worker(worker_id):
    return node_service.stop_worker(worker_id)

@node.route('/worker/<int:worker_id>', methods=['GET'])
@auth.login_required
def get_worker(worker_id):
    return node_service.get_worker(worker_id)

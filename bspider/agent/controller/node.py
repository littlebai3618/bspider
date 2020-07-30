"""
    封装查看节点信息操作为api
"""
from flask import Blueprint

from bspider.agent.service.node import NodeService
from bspider.core.api import auth
from .validators.worker_forms import RegisterForm

node = Blueprint('node_bp', __name__)

node_service = NodeService()

@node.route('/node', methods=['GET'])
def status():
    """node-status 路由无需保护"""
    return node_service.node_status()

@node.route('/worker', methods=['POST'])
@auth.login_required
def start_worker():
    form = RegisterForm()
    return node_service.start_worker(**form.to_dict())

@node.route('/worker/<int:worker_id>', methods=['DELETE'])
@auth.login_required
def stop_worker(worker_id):
    return node_service.stop_worker(worker_id)

@node.route('/worker/<int:worker_id>', methods=['GET'])
@auth.login_required
def get_worker(worker_id):
    return node_service.get_worker(worker_id)

# @Time    : 2019/7/17 2:23 PM
# @Author  : 白尚林
# @File    : node
# @Use     :
from flask import Blueprint

from agent.service.node import NodeService
from core.api import auth
from .validators.worker_forms import RegisterForm, CommonForm

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
    return node_service.start_worker(form.name.data, form.worker_type.data, form.coroutine_num.data)

@node.route('/worker', methods=['DELETE'])
@auth.login_required
def stop_worker():
    form = CommonForm()
    return node_service.stop_worker(form.name.data)

@node.route('/worker', methods=['GET'])
@auth.login_required
def get_worker():
    form = CommonForm()
    if form.is_all.data == 1:
        return node_service.get_workers()
    else:
        return node_service.get_worker(form.name.data)

# part 2 接口
@node.route('/worker/status', methods=['GET'])
@auth.login_required
def get_worker_status():
    return node_service.worker_status()

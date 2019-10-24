# @Time    : 2019/7/1 5:41 PM
# @Author  : 白尚林
# @File    : node
# @Use     : 节点控制层
"""
所有和 Agent 进行交互的操作收缩到 node 蓝图下
1. 提供注册接口用于注册新 node
2. 删除接口删除节点 node /delete => 停止节点下所有work => 删除worker 表中节点对应的所有信息 => 停止Agent进程(supervisor)
4. 查询接口查询 节点信息 /get =>  返回节点和节点下已经注册的所有worker信息
5. 停止节点
6. 启动节点

5. 在节点下启动并在master注册一个worker /agent/start => 启动进程 => 成功后注册进表单
6. 在节点下停止一个 worker /agent/stop => 停止进程 status 设置为0
7. 在节点下重启一个 worker /agent/restart => 停止进程、启动进程
8. 删除一个 worker /agent/delete => 停止进程并删除注册信息
9. 查询 worker /agent/get/ => 得到节点下所有 worker 信息
"""
from flask import Blueprint

from bspider.core.api import auth
from .validators import PageForm
from .validators.node_forms import AddNodeForm, UpdateNodeForm, AddWorkerForm, ChangeWorkerForm
from bspider.web_studio.service.node import Node

node = Blueprint('node_bp', __name__)

node_service = Node()


@node.route('/node', methods=['POST'])
@auth.login_required
def add_node():
    form = AddNodeForm()
    return node_service.add_node(form.node_ip.data, form.desc.data, form.name.data)


@node.route('/node/<int:node_id>', methods=['DELETE'])
@auth.login_required
def delete_node(node_id):
    return node_service.delete_node(node_id)


@node.route('/node/<int:node_id>', methods=['PATCH'])
@auth.login_required
def update_node(node_id):
    form = UpdateNodeForm()
    return node_service.update_node(node_id, **form.get_dict())


@node.route('/node', methods=['GET'])
@auth.login_required
def get_nodes():
    form = PageForm()
    return node_service.get_nodes(int(form.page.data), int(form.limit.data), form.search.data, form.sort.data)


@node.route('/node/<int:node_id>', methods=['GET'])
@auth.login_required
def get_node(node_id):
    return node_service.get_node(node_id)


@node.route('/worker', methods=['POST'])
@auth.login_required
def add_worker():
    form = AddWorkerForm()
    return node_service.add_worker(form.ip.data, form.name.data, form.type.data, form.description.data, int(form.status.data))


@node.route('/worker/<int:worker_id>', methods=['DELETE'])
@auth.login_required
def delete_worker(worker_id):
    return node_service.delete_worker(worker_id)


@node.route('/worker/<int:worker_id>', methods=['PATCH'])
@auth.login_required
def change_worker(worker_id):
    form = ChangeWorkerForm()
    return node_service.update_worker(worker_id, **form.get_dict())


@node.route('/worker', methods=['GET'])
@auth.login_required
def get_workers():
    """获取全部worker信息"""
    form = PageForm()
    return node_service.get_workers(int(form.page.data), int(form.limit.data), form.search.data, form.sort.data)


@node.route('/worker/<int:worker_id>', methods=['GET'])
@auth.login_required
def get_worker(worker_id):
    return node_service.get_worker(worker_id)

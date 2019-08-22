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

from core.api.exception import ParameterException
from .validators.node_forms import AddNodeForm, DeleteNodeForm, GetNodeForm, ChangeNodeForm, AddWorkerForm, \
    DeleteWorkerForm, ChangeWorkerForm, GetWorkerForm
from web_studio.service.node import Node

node = Blueprint('node_bp', __name__)

node_service = Node()


@node.route('/node', methods=['POST'])
# @Auth
def add_node():
    form = AddNodeForm()
    return node_service.add_node(form.node_ip.data, form.desc.data, form.name.data)


@node.route('/node', methods=['DELETE'])
# @Auth
def delete_node():
    form = DeleteNodeForm()
    return node_service.delete_node(form.node_ip.data)


@node.route('/node', methods=['PATCH'])
# @Auth
def change_node():
    form = ChangeNodeForm()
    print(form.get_dict())
    if form.op.data == 'start':
        return node_service.start_node(form.node_ip.data)
    elif form.op.data == 'stop':
        return node_service.stop_node(form.node_ip.data)
    else:
        return ParameterException(msg=f'unknow op:{form.op.data}')


@node.route('/node', methods=['GET'])
# @Auth
def get_nodes():
    return node_service.get_nodes()


@node.route('/node/<string:node_ip>', methods=['GET'])
# @Auth
def get_node(node_ip):
    return node_service.get_node(node_ip)


@node.route('/worker', methods=['POST'])
# @Auth
def add_worker():
    form = AddWorkerForm()
    return node_service.add_worker(form.node_ip.data, form.name.data, form.worker_type.data, form.desc.data)


@node.route('/worker', methods=['DELETE'])
# @Auth
def delete_worker():
    form = DeleteWorkerForm()
    return node_service.delete_worker(form.node_ip.data, form.name.data, form.worker_type.data)


@node.route('/worker', methods=['PATCH'])
# @Auth
def change_worker():
    form = ChangeWorkerForm()
    if form.op.data == 'start':
        return node_service.start_worker(form.node_ip.data, form.name.data, form.worker_type.data)
    elif form.op.data == 'stop':
        return node_service.stop_worker(form.node_ip.data, form.name.data, form.worker_type.data)
    else:
        return ParameterException(msg=f'unknow op:{form.op.data}')


@node.route('/worker', methods=['GET'])
# @Auth
def get_worker():
    form = GetWorkerForm()
    if form.is_all.data == 1:
        return node_service.get_worker(form.node_ip.data, form.name.data)
    else:
        return node_service.get_workers()
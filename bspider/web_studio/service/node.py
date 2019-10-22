# @Time    : 2019/7/1 11:09 AM
# @Author  : 白尚林
# @File    : node
# @Use     :
from bspider.core.api import BaseService, Conflict, NotFound, PostSuccess, DeleteSuccess, PatchSuccess, GetSuccess, \
    ParameterException
from bspider.core.lib import RemoteMixIn
from bspider.utils.exceptions import RemoteOPError
from bspider.web_studio.server import log
from bspider.web_studio.service.impl.node_impl import NodeImpl


class Node(BaseService, RemoteMixIn):

    def __init__(self):
        self.impl = NodeImpl()

    # node API
    def add_node(self, ip, desc, name):
        projects = self.serializer_project(self.impl.get_jobs())
        self.impl.add_node({'ip': ip, 'description': desc, 'name': name})
        log.info(f'add agent from {name}:{ip} success')
        return PostSuccess(msg=f'add agent from {name}:{ip} success', data=projects)

    def delete_node(self, node_ip):
        """supervisor 停止进程 删除节点信息"""
        try:
            # 整个删除操作是一个事务
            with self.impl.handler.session() as session:
                session.delete(*self.impl.delete_node('ip', node_ip, get_sql=True))
                session.delete(*self.impl.delete_worker('ip', node_ip, get_sql=True))
                if not self.op_stop_node(node_ip):
                    log.error(f'supervisor try stop process failed:{node_ip}')
                    raise Conflict(msg='supervisor try stop process failed', errno=20005)
            log.info(f'delete agent {node_ip} success')
            return DeleteSuccess()
        except Exception as e:
            log.error(f'delete node:{node_ip} failed {e}')
            return Conflict(msg=f'delete node:{node_ip} failed {e}', errno=20005)

    def stop_node(self, node_ip):
        if self.op_stop_node(node_ip):
            log.info(f'stop node:{node_ip} success')
            return PatchSuccess(msg=f'stop node:{node_ip} success')
        log.error(f'supervisor try stop node:{node_ip} failed')
        return Conflict(msg=f'supervisor try stop node:{node_ip} failed', errno=20006)

    def start_node(self, node_ip):
        if self.op_start_node(node_ip):
            log.info(f'stop update:{node_ip} success')
            return PatchSuccess(msg=f'start node:{node_ip} success')
        log.error(f'supervisor try start node:{node_ip} failed')
        return Conflict(msg=f'supervisor try start node:{node_ip} failed', errno=20007)

    def get_node(self, node_ip):
        """得到node列表，查询rpc获取supervisor进程状态，整合，返回"""
        infos = self.impl.get_node(node_ip)
        if infos:
            for info in infos:
                self.datetime_to_str(info)
                supervisor_node_info = self.op_get_node(info['ip'])
                info['description'] = '{}->{}'.format(info.pop('description'), supervisor_node_info.pop('description'))
                info.update(supervisor_node_info)
            return GetSuccess(msg='get node:{} status success', data=infos)
        log.error(f'this node:{node_ip} is not exist')
        return NotFound(msg=f'this node:{node_ip} is not exist', errno=20008)

    def get_nodes(self, page, limit, search, sort):
        if sort.upper() not in ['ASC', 'DESC']:
            return ParameterException(msg='sort must `asc` or `desc`')

        infos, total = self.impl.get_nodes(page, limit, search, sort)

        for info in infos:
            self.datetime_to_str(info)
            supervisor_node_info = self.op_get_node(info['ip'])
            info['description'] = '{}->{}'.format(info.pop('description'), supervisor_node_info.pop('description'))
            info.update(supervisor_node_info)

        return GetSuccess(
            msg='get nodes list success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })

    # worker API
    def add_worker(self, node_ip, name, worker_type, description):
        try:
            with self.impl.handler.session() as session:
                data = {
                    'ip': node_ip,
                    'name': name,
                    'type': worker_type,
                    'description': description,
                }
                session.insert(*self.impl.add_worker(data, get_sql=True))
                req = self.op_start_worker(node_ip, f'{worker_type}:{name}', worker_type)
                data['pid'] = req['pid']
                data['status'] = 1
            log.info(f'add a new worker:{name} success')
            return PostSuccess(msg='add a new worker success!', data=data)
        except Exception as e:
            log.error(f'add a new worker:{name} failed: {e}')
            return Conflict(msg=f'add a new worker failed: {e}', errno=20003)

    def stop_worker(self, node_ip, name, worker_type):
        if self.op_stop_worker(node_ip, f'{worker_type}:{name}'):
            log.info(f'stop worker:{name} success')
            return PostSuccess(msg='stop worker success!')
        log.error(f'stop worker:{name} failed')
        return Conflict(msg=f'stop worker failed', errno=20009)

    def start_worker(self, node_ip, name, worker_type):
        if self.op_start_worker(node_ip, f'{worker_type}:{name}', worker_type):
            log.info(f'start worker:{name} success')
            return PostSuccess(msg='start worker success!')
        log.error(f'start worker:{name} failed')
        return Conflict(msg=f'start worker failed', errno=20003)

    def delete_worker(self, node_ip, name, worker_type):
        try:
            # 整个删除操作是一个事务
            with self.impl.handler.session() as session:
                session.delete(*self.impl.delete_worker('name', name, get_sql=True))
                if not self.op_stop_worker(node_ip, f'{worker_type}:{name}', worker_type):
                    log.error(f'supervisor try stop process failed from {node_ip}')
                    raise Conflict(msg='supervisor try stop process failed', errno=20009)
            return DeleteSuccess()
        except Exception as e:
            log.error(f'delete node:{node_ip} failed {e}')
            return Conflict(msg=f'delete node:{node_ip} failed {e}', errno=20009)

    def get_worker(self, node_ip, name, worker_type):
        worker_info = self.op_get_worker(node_ip, f'{worker_type}:{name}')['data']
        mysql_node_info = self.impl.get_worker(name)
        if mysql_node_info:
            for key, value in mysql_node_info[0].items():
                worker_info[key] = value
            return GetSuccess(msg=f'get work:{node_ip}-{name} status success', data=worker_info)
        return NotFound(msg=f'this work:{node_ip}-{name} is not exist', errno=20008)

    def get_workers(self):
        result = []
        worker_infos = self.impl.get_workers()
        for worker in worker_infos:
            try:
                worker_info = self.op_get_worker(worker['ip'], '{}:{}'.format(worker['type'], worker['name']))
            except RemoteOPError:
                worker_info = dict(mem=0.0, status=False, pid=None, is_run=False)
            worker_info['ip'] = worker['ip']
            worker_info['name'] = worker['name']
            result.append(worker_info)
        return GetSuccess(msg='get all worker status success', data=result)

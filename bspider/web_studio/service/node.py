# @Time    : 2019/7/1 11:09 AM
# @Author  : 白尚林
# @File    : node
# @Use     :
from bspider.core.api import BaseService, Conflict, NotFound, PostSuccess, DeleteSuccess, PatchSuccess, GetSuccess, \
    ParameterException
from bspider.core.api import AgentMixIn
from bspider.utils.exceptions import RemoteOPError
from bspider.web_studio.server import log
from bspider.web_studio.service.impl.node_impl import NodeImpl


class Node(BaseService, AgentMixIn):

    def __init__(self):
        self.impl = NodeImpl()

    # node API
    def add_node(self, ip, desc, name):
        self.impl.add_node({'ip': ip, 'description': desc, 'name': name})
        log.info(f'add agent from {name}:{ip} success')
        return PostSuccess(
            msg=f'add agent from {name}:{ip} success',
            data={
                'projects': self.impl.get_all_projects(),
                'codes': self.impl.get_all_codes(),
                'workers': self.impl.get_all_workers(ip)
            })

    def delete_node(self, node_id):
        """supervisor 停止进程 删除节点信息"""
        nodes = self.impl.get_node(node_id)
        if not len(nodes):
            log.error(f'node is not exist')
            return Conflict(msg=f'node is not exist', errno=20008)
        node = nodes[0]
        try:
            # 整个删除操作是一个事务
            with self.impl.handler.session() as session:
                session.delete(*self.impl.delete_node(node_id, get_sql=True))
                session.delete(*self.impl.delete_worker_by_ip(node['ip'], get_sql=True))
                self.op_stop_node(node['ip'])
            log.info(f'delete node success')
            return DeleteSuccess()
        except Exception as e:
            log.error('delete node:{} failed {}'.format(node['name'], e))
            return Conflict(msg='delete node:{} failed {}'.format(node['name'], e), errno=20005)

    def update_node(self, node_id, **kwargs):
        nodes = self.impl.get_node(node_id)
        if not len(nodes):
            log.error(f'node is not exist')
            return Conflict(msg=f'node is not exist', errno=20008)
        node = nodes[0]
        try:
            remote_change = False
            for key in ('status',):
                if key in kwargs:
                    remote_change = True
                    break

            status = kwargs.pop('status')

            if remote_change:
                with self.impl.handler.session() as session:
                    if len(kwargs):
                        session.update(*self.impl.update_node(node_id, kwargs, get_sql=True))
                    if status == 'start':
                        self.op_start_node(node['ip'])
                    elif status == 'stop':
                        self.op_stop_node(node['ip'])

            elif len(kwargs):
                self.impl.update_node(node_id, kwargs)
            return PatchSuccess(msg='update node:{name} success'.format(**node))

        except Exception as e:
            log.error('update node:{} failed {} {}'.format(node['ip'], e, kwargs))
            return Conflict(msg='update node:{} failed {}'.format(node['ip'], e), errno=20005)

    def get_node(self, node_id):
        """得到node列表，查询rpc获取supervisor进程状态，整合，返回"""
        infos = self.impl.get_node(node_id)
        if infos:
            for info in infos:
                self.datetime_to_str(info)
                supervisor_node_info = self.op_get_node(info['ip'])
                info['description'] = '{}->{}'.format(info.pop('description'), supervisor_node_info.pop('description'))
                info.update(supervisor_node_info)
            return GetSuccess(msg='get node:{} status success', data=infos)
        log.error(f'this node id={node_id} is not exist')
        return NotFound(msg=f'this node id={node_id} is not exist', errno=20008)

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
    def add_worker(self, node_ip, name, worker_type, description, status):
        """携程数量更新很麻烦所以这里写死"""
        try:
            with self.impl.handler.session() as session:
                coroutine_num = 50 if worker_type == 'downloader' else 4
                data = {
                    'ip': node_ip,
                    'name': name,
                    'type': worker_type,
                    'description': description,
                    'coroutine_num': coroutine_num,
                    'status': status
                }
                session.insert(*self.impl.add_worker(data, get_sql=True))
                if status == 1:
                    req = self.op_start_worker(node_ip, f'{worker_type}:{name}', worker_type, coroutine_num)
                    data['pid'] = req['pid']
                else:
                    data['pid'] = 0

            log.info(f'add a new worker:{name} success')
            return PostSuccess(msg='add a new worker success!', data=data)
        except RemoteOPError as e:
            log.error(f'add a new worker:{name} failed: {e}')
            return Conflict(msg=f'add a new worker failed: {e}', errno=20003)

    def update_worker(self, worker_id, **kwargs):
        """
        name, ip
        :param worker_id:
        :param kwargs:
        :return:
        """
        workers = self.impl.get_worker(worker_id)
        if not len(workers):
            log.error(f'worker is not exist')
            return Conflict(msg=f'worker is not exist', errno=20004)
        worker = workers[0]

        try:
            remote_change = False
            for key in ('ip', 'type', 'status', 'coroutine_num'):
                if key in kwargs:
                    remote_change = True
                    break

            if remote_change:
                with self.impl.handler.session() as session:
                    session.update(*self.impl.update_worker(worker_id, kwargs, get_sql=True))
                    if worker['status'] == 1:
                        self.op_stop_worker(worker['ip'], '{}:{}'.format(worker['type'], worker['name']))
                        if kwargs.get('status') == 1:
                            self.op_start_worker(
                                ip=kwargs.get('ip', worker['ip']),
                                worker_type=kwargs.get('type', worker['type']),
                                unique_sign='{}:{}'.format(kwargs.get('type', worker['type']),
                                                           kwargs.get('name', worker['name'])),
                                coroutine_num=kwargs.get('coroutine_num', worker['coroutine_num'])
                            )
                    elif worker['status'] == 0 and kwargs.get('status') == 1:
                        self.op_start_worker(
                            ip=kwargs.get('ip', worker['ip']),
                            worker_type=kwargs.get('type', worker['type']),
                            unique_sign='{}:{}'.format(kwargs.get('type', worker['type']),
                                                       kwargs.get('name', worker['name'])),
                            coroutine_num=kwargs.get('coroutine_num', worker['coroutine_num'])
                        )

            elif len(kwargs):
                self.impl.update_worker(worker_id, kwargs)
            return PatchSuccess(msg='update worker:{name} success'.format(**worker))

        except RemoteOPError as e:
            log.error('update worker:{} failed {}'.format(worker['ip'], e))
            return Conflict(msg='update worker:{} failed {}'.format(worker['ip'], e), errno=20005)

    def delete_worker(self, worker_id):
        workers = self.impl.get_worker(worker_id)
        if not len(workers):
            log.error(f'worker is not exist')
            return Conflict(msg=f'worker is not exist', errno=20004)
        worker = workers[0]

        try:
            # 整个删除操作是一个事务
            with self.impl.handler.session() as session:
                session.delete(*self.impl.delete_worker_by_id(worker_id, get_sql=True))
                self.op_stop_worker(worker['ip'], '{}:{}'.format(worker['type'], worker['name']))
            return DeleteSuccess()
        except RemoteOPError as e:
            log.error('delete worker:{} failed {}'.format(worker['ip'], e))
            return Conflict(msg='delete worker:{} failed {}'.format(worker['ip'], e), errno=20009)

    def get_worker(self, worker_id):
        infos = self.impl.get_worker(worker_id)
        if len(infos):
            for info in infos:
                self.datetime_to_str(info)
                try:
                    worker_status = self.op_get_worker(info['ip'], '{}:{}'.format(info['type'], info['name']))
                except RemoteOPError:
                    worker_status = dict(mem=0.0, status=False, pid=None, is_run=False)
                info.update(worker_status)
            return GetSuccess(msg=f'get worker status success', data=infos)
        return NotFound(msg=f'this worker id={worker_id} is not exist', errno=20008)

    def get_workers(self, page, limit, search, sort):
        if sort.upper() not in ['ASC', 'DESC']:
            return ParameterException(msg='sort must `asc` or `desc`')

        infos, total = self.impl.get_workers(page, limit, search, sort)
        for info in infos:
            self.datetime_to_str(info)
            try:
                worker_status = self.op_get_worker(info['ip'], '{}:{}'.format(info['type'], info['name']))
            except RemoteOPError:
                worker_status = dict(mem=0.0, status=-1, pid=None, is_run=False)
            info.update(worker_status)
        return GetSuccess(
            msg='get worker status success!',
            data={
                'items': infos,
                'total': total,
                'page': page,
                'limit': limit
            })

# # Inner func
# def __stop_node(self, node_ip):
#     if self.op_stop_node(node_ip):
#         log.info(f'stop node:{node_ip} success')
#         return PatchSuccess(msg=f'stop node:{node_ip} success')
#     log.error(f'supervisor try stop node:{node_ip} failed')
#     return Conflict(msg=f'supervisor try stop node:{node_ip} failed', errno=20006)
#
#
# def __start_node(self, node_ip):
#     if self.op_start_node(node_ip):
#         log.info(f'stop update:{node_ip} success')
#         return PatchSuccess(msg=f'start node:{node_ip} success')
#     log.error(f'supervisor try start node:{node_ip} failed')
#     return Conflict(msg=f'supervisor try start node:{node_ip} failed', errno=20007)

# def stop_worker(self, node_ip, name, worker_type):
#     if self.op_stop_worker(node_ip, f'{worker_type}:{name}'):
#         log.info(f'stop worker:{name} success')
#         return PostSuccess(msg='stop worker success!')
#     log.error(f'stop worker:{name} failed')
#     return Conflict(msg=f'stop worker failed', errno=20009)
#
#
# def start_worker(self, node_ip, name, worker_type):
#     if self.op_start_worker(node_ip, f'{worker_type}:{name}', worker_type):
#         log.info(f'start worker:{name} success')
#         return PostSuccess(msg='start worker success!')
#     log.error(f'start worker:{name} failed')
#     return Conflict(msg=f'start worker failed', errno=20003)

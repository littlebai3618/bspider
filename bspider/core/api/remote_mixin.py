import json
import xmlrpc.client

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from flask import g

from bspider.config import FrameSettings
from bspider.core.api.auth.token import make_token
from bspider.utils.exceptions import RemoteOPError


class RemoteMixIn(object):
    # 可以优化为协程方式调用

    @staticmethod
    def request(url, method, params=None, data=None, token=None):
        if token:
            headers = dict(Authorization=f'Bearer {token}')
        else:
            headers = dict(Authorization=f'Bearer {g.user.token}')
        if data:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(data)
        try:
            req = requests.request(method, url, headers=headers, data=data, params=params)
        except ConnectionError as e:
            raise RemoteOPError('Call Remote failed please check!, error:%s' % (e))
        return req


class AgentMixIn(RemoteMixIn):
    """
    master -> agent 主节点向子节点进行通信
    """
    base_url = 'http://{}:' + str(FrameSettings()['AGENT'].get('port', 5001)) + '{}'
    rpc_url = 'http://{username}:{password}@%s:{port}/RPC2'.format(**FrameSettings()['SUPERVISOR_RPC'])

    def op_stop_node(self, ip: str) -> bool:
        with xmlrpc.client.ServerProxy(self.rpc_url % ip) as rpc_server:
            if rpc_server.supervisor.stopProcess('agent:agent'):
                return True
        return False

    def op_start_node(self, ip: str) -> bool:
        with xmlrpc.client.ServerProxy(self.rpc_url % ip) as rpc_server:
            if rpc_server.supervisor.startProcess('agent:agent'):
                return True
        return False

    def op_get_node(self, ip: str) -> dict:
        result = {
            'description': f'Agent {ip} process is not exist!!!',
            'pid': 0,
            'status': -1
        }

        with xmlrpc.client.ServerProxy(self.rpc_url % ip) as rpc_server:
            process = rpc_server.supervisor.getAllProcessInfo()[0]
            if process['name'] == 'agent':
                result['description'] = process['description']
                result['pid'] = process['pid']
                if process['state'] == 20:
                    result['status'] = 1
                elif process['state'] == 0:
                    result['status'] = 0
                else:
                    result['description'] = 'Error see->{}'.format(process['stdout_logfile'])
                    result['pid'] = process['pid']
                return result
        return result

    def op_stop_worker(self, ip: str, worker_id: int, token: str = None) -> bool:
        url = self.base_url.format(ip, f'/worker/{worker_id}')
        req = self.request(url, method='DELETE', token=token)
        if req.status_code == 204:
            return True
        raise RemoteOPError('stop work error %s' % (req.json()['msg']))

    def op_start_worker(self, ip: str, worker_id: int, worker_type: str, coroutine_num: int, token: str = None) -> dict:
        url = self.base_url.format(ip, '/worker')
        data = {
            'worker_id': worker_id,
            'worker_type': worker_type,
            'coroutine_num': coroutine_num
        }
        req = self.request(url, method='POST', data=data, token=token)
        data = req.json()
        if data['errno'] == 0:
            return data['data']

    def op_get_worker(self, ip: str, worker_id: int, token: str = None) -> dict:
        url = self.base_url.format(ip, f'/worker/{worker_id}')
        req = self.request(url, method='GET', token=token)
        data = req.json()
        if data['errno'] == 0:
            return data['data']
        raise RemoteOPError('get worker error %s' % (req.json()['msg']))

    def __op_query(self, ip_list: list, method: str, uri: str, data: dict = None, token: str = None) -> (bool, dict):
        result = dict()
        if method == 'DELETE':
            for ip in ip_list:
                req = self.request(self.base_url.format(ip, uri), method=method, data=data, token=token)
                if not (req.status_code >= 200 and req.status_code <= 299):
                    result[ip] = req.json()['msg']
        else:
            for ip in ip_list:
                data = self.request(self.base_url.format(ip, uri), method=method, data=data, token=token).json()
                if data['errno'] != 0:
                    result[ip] = data['msg']
        return not len(result), result

    def op_add_project(self, ip_list: list, data: dict, token: str = None) -> (bool, dict):
        # project_id, name, config, rate, status
        return self.__op_query(ip_list, 'POST', '/project', data, token=token)

    def op_update_project(self, ip_list: list, project_id: int, data: dict, token: str = None) -> (bool, dict):
        return self.__op_query(ip_list, 'PATCH', f'/project/{project_id}', data, token=token)

    def op_delete_project(self, ip_list: list, project_id: int, token: str = None) -> (bool, dict):
        return self.__op_query(ip_list, 'DELETE', f'/project/{project_id}', token=token)

    def op_add_code(self, ip_list: list, data: dict, token: str = None) -> (bool, dict):
        # code_id, content
        return self.__op_query(ip_list, 'POST', '/code', data, token=token)

    def op_update_code(self, ip_list: list, code_id: int, data: dict, token: str = None) -> (bool, dict):
        return self.__op_query(ip_list, 'PATCH', f'/code/{code_id}', data, token=token)

    def op_delete_code(self, ip_list: list, code_id: int, token: str = None) -> (bool, dict):
        return self.__op_query(ip_list, 'DELETE', f'/code/{code_id}', token=token)

    def op_get_node_status(self, ip: int):
        url = self.base_url.format(ip, f'/node')
        req = self.request(url, method='GET', token='operation-token')
        data = req.json()
        if data['errno'] == 0:
            return data['data']
        raise RemoteOPError('get worker error %s' % (req.json()['msg']))


class MasterMixIn(RemoteMixIn):
    """
    agent -> master 主节点向子节点进行通信
    """

    base_url = 'http://{ip}:{port}/node'.format(**FrameSettings()['MASTER'])

    def op_add_node(self, data: dict, token: str = None) -> dict:
        data = self.request(
            self.base_url,
            method='POST',
            data=data,
            token=token if token else make_token(0, 'agent')
        ).json()
        if data['errno'] == 0:
            return data['data']

        raise RemoteOPError('Call Master Failed to reg node msg %s' % (data['msg']))


class RabbitMQMixIn(object):
    authorization = HTTPBasicAuth(FrameSettings()['RABBITMQ_MANAGEMENT_CONFIG']['username'],
                                  FrameSettings()['RABBITMQ_MANAGEMENT_CONFIG']['password'])
    virtual_host = FrameSettings()['RABBITMQ_CONFIG']['virtual_host']
    base_url = '{}/%s'.format(FrameSettings()['RABBITMQ_MANAGEMENT_CONFIG']['address'])

    def request(self, url, method, params=None, data=None):
        headers = {'Content-Type': 'application/json'}
        if data:
            data = json.dumps(data)
        try:
            req = requests.request(method, url, headers=headers, data=data, params=params, auth=self.authorization)
        except ConnectionError as e:
            raise RemoteOPError(f'Call RabbitMQ Management plug-in failed please check!, error:%s' % (e))
        return req

    def op_get_project_queue_detail(self, project_id: int):
        """根据project_id 获取队列的信息"""
        uri = f'api/queues/{self.virtual_host}'
        req = self.request(self.base_url % uri, 'GET', params={'name': f'_{project_id}'})
        if req.status_code == 200:
            return req.json()
        raise RemoteOPError('get queue info Failed %s' % (req.text))

    def op_purge_queue_msg(self, project_id: int):
        uri = f'api/queues/bspider/candidate_{project_id}/contents'
        req = self.request(self.base_url % uri, 'DELETE', params={"vhost": self.virtual_host,"name":f"candidate_{project_id}","mode":"purge"})
        if req.status_code == 204:
            return None
        raise RemoteOPError('purge queue info Failed %s' % (req.text))



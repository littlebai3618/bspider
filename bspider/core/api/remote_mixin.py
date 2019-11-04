# @Time    : 2019/7/18 3:51 PM
# @Author  : 白尚林
# @File    : remote_mixin
# @Use     :
import json
import xmlrpc.client

import requests
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
            raise RemoteOPError(f'Call Remote failed please check!, error:{e}')
        return req


class AgentMixIn(RemoteMixIn):
    """
    master -> agent 主节点向子节点进行通信
    """
    base_url = 'http://{}:' + str(FrameSettings()['AGENT'].get('port', 5001)) + '{}'
    rpc_url = 'http://{username}:{password}@%s:{port}/RPC2'.format(**FrameSettings()['SUPERVISOR_RPC'])

    def op_stop_node(self, ip) -> bool:
        with xmlrpc.client.ServerProxy(self.rpc_url % ip) as rpc_server:
            if rpc_server.supervisor.stopProcess('agent:agent'):
                return True
        return False

    def op_start_node(self, ip) -> bool:
        with xmlrpc.client.ServerProxy(self.rpc_url % ip) as rpc_server:
            if rpc_server.supervisor.startProcess('agent:agent'):
                return True
        return False

    def op_get_node(self, ip) -> dict:
        result = {
            'description': 'no process name agent',
            'pid': -1,
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
                    result['description'] = 'error in this node log:{}'.format(process['stdout_logfile'])
                    result['pid'] = process['pid']
                return result
        return result

    def op_stop_worker(self, ip: str, unique_sign: str) -> bool:
        url = self.base_url.format(ip, '/worker')
        data = {'name': unique_sign}
        req = self.request(url, method='DELETE', params=data)
        if req.status_code == 204:
            return True
        raise RemoteOPError('stop work error {}', req.json()['msg'])

    def op_start_worker(self, ip: str, unique_sign: str, worker_type: str, coroutine_num: int) -> dict:
        url = self.base_url.format(ip, '/worker')
        data = {
            'name': unique_sign,
            'worker_type': worker_type,
            'coroutine_num': coroutine_num
        }
        req = self.request(url, method='POST', data=data)
        data = req.json()
        if data['errno'] == 0:
            return data['data']
        raise RemoteOPError('start work error {}', data['msg'])

    def op_get_worker(self, ip: str, worker_id: str) -> dict:
        url = self.base_url.format(ip, '/worker')
        req = self.request(url, method='GET', params={'worker_id': worker_id, 'is_all': 1})
        data = req.json()
        if data['errno'] == 0:
            return data['data'] if data.get('data') else {}
        raise RemoteOPError('get worker error {}', data['msg'])

    def __op_query(self, ip_list: list, method: str, uri: str, data: dict = None) -> (bool, dict):
        result = dict()
        if method == 'DELETE':
            for ip in ip_list:
                req = self.request(self.base_url.format(ip, uri), method=method, data=data)
                if not (req.status_code >= 200 and req.status_code <= 299):
                    result[ip] = req.json()['msg']
        else:
            for ip in ip_list:
                data = self.request(self.base_url.format(ip, uri), method=method, data=data).json()
                if data['errno'] != 0:
                    result[ip] = data['msg']
        return not len(result), result

    def op_add_project(self, ip_list: list, data: dict) -> (bool, dict):
        # project_id, name, config, rate, status
        return self.__op_query(ip_list, 'POST', '/project', data)

    def op_update_project(self, ip_list: list, project_id: int, data: dict) -> (bool, dict):
        return self.__op_query(ip_list, 'PATCH', f'/project/{project_id}', data)

    def op_delete_project(self, ip_list: list, project_id: int) -> (bool, dict):
        return self.__op_query(ip_list, 'DELETE', f'/project/{project_id}')

    def op_add_code(self, ip_list: list, data: dict) -> (bool, dict):
        # code_id, content
        return self.__op_query(ip_list, 'POST', '/code', data)

    def op_update_code(self, ip_list: list, code_id: int, data: dict) -> (bool, dict):
        return self.__op_query(ip_list, 'PATCH', f'/code/{code_id}', data)

    def op_delete_code(self, ip_list: list, code_id: int) -> (bool, dict):
        return self.__op_query(ip_list, 'DELETE', f'/code/{code_id}')


class MasterMixIn(RemoteMixIn):
    """
    agent -> master 主节点向子节点进行通信
    """

    base_url = 'http://{ip}:{port}/node'.format(**FrameSettings()['MASTER'])

    def op_add_node(self, data: dict) -> dict:
        data = self.request(
            self.base_url,
            method='POST',
            data=data,
            token=make_token(0, 'agent')
        ).json()
        if data['errno'] == 0:
            return data['data']

        raise RemoteOPError('Call Master Failed to reg node msg {}', data['msg'])

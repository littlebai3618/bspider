# @Time    : 2019/7/18 3:51 PM
# @Author  : 白尚林
# @File    : remote_mixin
# @Use     :
import json
import xmlrpc.client

import requests
from flask import g

from bspider.config import FrameSettings
from bspider.utils.exceptions import RemoteOPError


class RemoteMixIn(object):

    base_url = 'http://{}:{}{}'
    port = 5001
    rpc_url = 'http://{username}:{password}@%s:{port}/RPC2'.format(**FrameSettings()['SUPERVISOR_RPC'])

    @staticmethod
    def request(url, method, params=None, data=None):
        if data is None:
            headers=None
        else:
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {g.user.token}'}
        req = requests.request(method, url, headers=headers, data=data, params=params)
        return req

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

    def op_restart(self, ip) -> bool:
        with xmlrpc.client.ServerProxy(self.rpc_url % ip) as rpc_server:
            if rpc_server.supervisor.stopProcess('agent:agent'):
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


    def op_stop_worker(self, ip: str, unique_sign: str, port: int=5001) -> bool:
        url = self.base_url.format(ip, port, '/worker')
        data = {'name': unique_sign}
        req = self.request(url, method='DELETE', params=data)
        if req.status_code == 204:
            return True
        raise RemoteOPError('stop work error {}', req.json()['msg'])

    def op_start_worker(self, ip: str,unique_sign: str, worker_type: str, port: int=5001) -> dict:
        url = self.base_url.format(ip, port, '/worker')
        data = {
            'name': unique_sign,
            'worker_type': worker_type
        }
        if worker_type == 'downloader':
            data['coroutine_num'] = 50
        else:
            data['coroutine_num'] = 4
        req = self.request(url, method='POST', data=json.dumps(data))
        data = req.json()
        if data['errno'] == 0:
            return data['data']
        raise RemoteOPError('start work error {}', data['msg'])

    def op_get_worker(self, ip: str, worker_name: str, port: int=5001) -> dict:
        url = self.base_url.format(ip, port, f'/worker')
        req = self.request(url, method='GET', params={'name': worker_name, 'is_all': 1})
        data = req.json()
        print(data)
        if data['errno'] == 0:
            return data['data'] if data.get('data') else {}
        raise RemoteOPError('get worker error {}', data['msg'])

    def op_add_project(self, ip_list: list, data, port: int=5001) -> dict:
        result = {}
        for ip in ip_list:
            url = self.base_url.format(ip, port, '/project')
            req = self.request(url, method='POST', data=json.dumps(data))
            print(url, json.dumps(data))
            data = req.json()
            if data['errno'] != 0:
                result[ip] = data['msg']
        return result

    def op_update_project(self, ip_list: list, data, port: int=5001) -> dict:
        result = {}
        for ip in ip_list:
            url = self.base_url.format(ip, port, '/project')
            req = self.request(url, method='PATCH', data=json.dumps(data))
            data = req.json()
            if data['errno'] != 0:
                result[ip] = data['msg']
        return result

    def op_delete_project(self, ip_list: list, project_id, port: int=5001) -> dict:
        result = {}
        for ip in ip_list:
            url = self.base_url.format(ip, port, f'/project/{project_id}')
            req = self.request(url, method='DELETE')
            if not (req.status_code >= 200 and req.status_code <=299):
                result[ip] = req.json()['msg']
        return result

    def op_update_code(self, ip_list: list, data, port: int=5001) -> dict:
        result = {}
        for ip in ip_list:
            url = self.base_url.format(ip, port, f'/project/code')
            req = self.request(url, method='PATCH', data=json.dumps(data))
            if not (req.status_code >= 200 and req.status_code <= 299):
                result[ip] = req.json()['msg']
        return result





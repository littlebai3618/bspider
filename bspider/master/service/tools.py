# @Time    : 2019/7/11 6:51 PM
# @Author  : 白尚林
# @File    : tools
# @Use     : 工具类
"""
1. 获取node ip列表 /tools/nodelist [{name: , ip:}]
"""
import base64
import json
import zlib

from apscheduler.triggers.cron import CronTrigger

from bspider.core.api import BaseService, GetSuccess, NotFound, AgentMixIn

from .impl.tools_impl import ToolsImpl


class ToolsService(BaseService, AgentMixIn):

    def __init__(self):
        self.impl = ToolsImpl()

    def get_node_list(self):
        """获取节点列表"""
        infos = self.impl.get_node_list()
        return GetSuccess(msg='get code success', data=infos)

    def get_code_list(self, code_type):
        infos = self.impl.get_code_list(code_type)
        return GetSuccess(msg='get code success', data=infos)

    def validate(self, valid_type, data):
        if valid_type == 'crontab':
            try:
                CronTrigger.from_crontab(data)
                return GetSuccess(msg='validate complete', data={'valid': True})
            except Exception:
                return GetSuccess(msg='validate complete', data={'valid': False})
        return NotFound(msg='unknow validate type', errno=60001)

    def node_status(self, ip):
        """调用接口返回节点状态，兼职探活"""
        return GetSuccess(data=self.op_get_node_status(ip))

    def get_parser_exception(self, project_id):
        infos = self.impl.get_parser_exception(project_id)
        for info in infos:
            self.datetime_to_str(info)
            if info['exception']:
                info['exception'] = info['exception'].replace('\n', '<br>')
        return GetSuccess(data=infos)

    def get_downloader_exception(self, project_id):
        infos = self.impl.get_downloader_exception(project_id)
        for info in infos:
            self.datetime_to_str(info)
            if info['exception']:
                info['exception'] = info['exception'].replace('\n', '<br>')
        return GetSuccess(data=infos)

    def get_crawl_detail(self, tag, source, data):
        if tag == 'sign':
            infos = self.impl.get_crawl_detail(data, source)
        else:
            sign = self.impl.get_sign_by_url(data)
            if sign:
                infos = self.impl.get_crawl_detail(sign, source)
            else:
                return NotFound(errno=60002, msg=f'NotFound url:{data}')

        for info in infos:
            self.datetime_to_str(info)
            if info['response'] is not None:
                info['response'] = json.loads(zlib.decompress(base64.b64decode(infos[0]['response'])).decode())
            return GetSuccess(data=info)
        return NotFound(errno=60002, msg=f'NotFound tag:{data}')

    def get_node_detail(self):
        return GetSuccess(data=self.impl.get_node_detail()[0])

    def get_exception_project(self):
        return GetSuccess(data=self.impl.get_exception_project())

    def get_code_type_detail(self):
        return GetSuccess(data=self.impl.get_code_type_detail())



    def get_request_track(self, url=None, sign=None):
        if url:
            sign = self.impl.get_sign_by_url(url)

        if sign:
            track_info = self.impl.get_reqest_track(sign)
            return 0, f'查询成功', track_info

    def parser_error(self, error):
        for err in error:
            err['size'] = 'large'
            err['timestamp'] = err['crawl_time']
            if err['status'] == 599:
                err['type'] = 'warning'
            else:
                err['type'] = 'danger'

            if err['status'] == -1:
                err['status'] = 'FAIL'
            if err['exception']:
                err['exception'] = err['exception'].replace('\n\n', '<br>')
        return error

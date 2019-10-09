# @Time    : 2019/7/11 6:51 PM
# @Author  : 白尚林
# @File    : tools
# @Use     : 工具类
from bspider.core.api import BaseService
from bspider.web_studio.service.impl.tools_impl import ToolsImpl


class ToolsService(BaseService):

    def __init__(self):
        self.impl = ToolsImpl()

    def get_parser_error(self, project_name):
        error = self.impl.get_parser_error(project_name)
        return 0, f'查询{project_name}成功', self.parser_error(error)

    def get_downloader_error(self, project_name):
        error = self.impl.get_downloader_error(project_name)
        return 0, f'查询{project_name}成功', self.parser_error(error)

    def get_reqest_track(self, url=None, sign=None):
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

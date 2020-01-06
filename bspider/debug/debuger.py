import asyncio
import os
from os.path import abspath
from queue import Queue

import yaml

from bspider.config import FrameSettings
from bspider.core import Project
from bspider.master.controller.validators.project_form import schema
from bspider.downloader.async_downloader import AsyncDownloader
from bspider.parser.async_parser import AsyncParser
from bspider.http import Request
from bspider.utils.conf import PLATFORM_PATH_ENV
from bspider.utils.exceptions import ModuleExistError
from bspider.utils.database import MysqlClient
from bspider.utils.logger import LoggerPool
from bspider.utils.sign import Sign
from bspider.utils.tools import find_class_name_by_content


class Debuger(object):
    """继承此类进行BSpider 框架的开发调试"""
    frame_settings = FrameSettings()

    # 最大下载次数 下载超过此数量个 Request 调试进程会终止
    max_follow_url_num = 10
    # 调试的url链接
    start_request = Request('http://127.0.0.1')

    # proority fix rabbitmq 数字越大优先级越高，使用Python优先队列模拟的时候需要进行优先级翻转

    def __init__(self):
        self.debug_log_fn = 'terminal'
        self.log = LoggerPool().get_logger(
            key=self.project_name,
            module='debuger',
            project=self.project_name,
            fn=self.debug_log_fn
        )
        self.mysql_client = MysqlClient.from_settings(self.frame_settings.get('WEB_STUDIO_DB'))
        self.local_project_class = self.__find_local_class()

        self.max_priority = self.frame_settings['QUEUE_ARG'].get('x-max-priority', 5)
        self.priority_queue = [Queue() for _ in range(self.max_priority)]

        self.put(self.start_request)

        with open(abspath('settings.yaml')) as f:
            self.project = Project(schema(yaml.safe_load(f)),
                                   middleware_serializer_method=self.check_module,
                                   pipeline_serializer_method=self.check_module)
            self.project.project_id = 0

        self.parser = AsyncParser(self.project, Sign(), self.debug_log_fn)
        self.log.info('init parser success')
        self.downloader = AsyncDownloader(self.project, Sign(), self.debug_log_fn)
        self.log.info('init downloader success')
        self.__cur_download_num = 1

    @property
    def project_name(self):
        return os.path.basename(os.getcwd())

    def put(self, request: Request):
        """向优先队列中存入req"""
        try:
            self.priority_queue[self.max_priority - request.priority].put(request)
        except KeyError as e:
            self.log.error(
                f'At req:{request.url}, requests.priority={request.priority} must between 1~{self.max_priority}')
            raise e

    def get(self):
        """从优先队列中取出req，若空则返回None"""
        for i in range(self.max_priority - 1, -1, -1):
            if self.priority_queue[i].empty():
                continue
            return self.priority_queue[i].get()

    def start(self):
        """调试入口"""
        tasks = [asyncio.ensure_future(self.__debug())]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

        self.log.info('debuger finished')

    async def __debug(self):
        while True:
            request = self.get()
            if request is None:
                self.log.debug('candidate queue is empty')
                break

            self.log.info(f'start download url:{request.url}')
            response, sign, _ = await self.downloader.download(request)
            self.__cur_download_num += 1
            if sign:
                self.log.info(f'start parser url:{response.url} status:{response.status}')
                reqs = await self.parser.parse(response)
                for req in reqs:
                    self.put(req)

            if self.__cur_download_num > self.max_follow_url_num:
                self.log.info(f'debuger follow url {self.max_follow_url_num} second')
                break

    def __find_local_class(self):
        # 将模块名称转换为模块代码
        local_project_class = dict()

        project_path = os.path.join(os.environ[PLATFORM_PATH_ENV], 'projects', self.project_name)
        for file in os.listdir(project_path):
            if not file.endswith('.py'):
                continue
            file_path = os.path.join(project_path, file)
            with open(file_path) as f:
                content = f.read().strip()
                class_name, sub_class = find_class_name_by_content(content)

            if sub_class in ('BaseMiddleware', 'BaseExtractor', 'BasePipeline'):
                self.log.debug(f'success find module:{class_name} from local')
                local_project_class[class_name] = content
        return local_project_class

    def load_remote_module(self, class_name):
        """加载远程代码"""
        sql = "select `content` from `{}` where `name`=%s;".format(self.frame_settings['CODE_STORE_TABLE'])
        info = self.mysql_client.select(sql, (class_name))
        if len(info):
            self.log.debug(f'success find module:{class_name} from remote')
            return class_name, info[0]['content']
        else:
            raise ModuleExistError('load module from remote failed %s is not exists' % (class_name))

    def check_module(self, cls_name):
        if cls_name in self.local_project_class:
            return cls_name, self.local_project_class[cls_name]
        return self.load_remote_module(cls_name)


if __name__ == '__main__':
    for i in range(10, 0):
        print(i)
        'ProjectConfigError'

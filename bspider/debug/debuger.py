import asyncio
import inspect
import os
from importlib import import_module
from os.path import abspath
from queue import Queue

import yaml

from bspider.config import FrameSettings
from bspider.core import Project
from bspider.master.controller.validators.project_form import schema
from bspider.downloader.async_downloader import AsyncDownloader
from bspider.parser.async_parser import AsyncParser
from bspider.http import Request
from bspider.utils.conf import PLATFORM_NAME_ENV
from bspider.utils.exceptions import ModuleExistError, ParserError
from bspider.utils.database import MysqlClient
from bspider.utils.logger import LoggerPool
from bspider.utils.sign import Sign
from bspider.utils.tools import class_name2module_name


class Debuger(object):
    """继承此类进行BSpider 框架的开发调试"""
    frame_settings = FrameSettings()

    # 最大下载次数 下载超过此数量个 Request 调试进程会终止
    max_follow_url_num = 10

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

        self.max_priority = self.frame_settings['QUEUE_ARG'].get('x-max-priority', 5)
        self.priority_queue = [Queue() for _ in range(self.max_priority)]

        with open(abspath('settings-development.yml'), encoding='utf8') as f:
            self.project = Project(schema(yaml.safe_load(f)),
                                   middleware_serializer_method=self.load_module,
                                   pipeline_serializer_method=self.load_module)
            self.project.project_id = 0

        self.parser = AsyncParser(self.project, Sign(), self.debug_log_fn)
        self.log.info('init parser success')
        self.downloader = AsyncDownloader(self.project, Sign(), self.debug_log_fn)
        self.log.info('init downloader success')
        self.__cur_download_num = 0
        self.log.info('send Request to queue')
        for extractor in self.parser.pipes:
            count = 0
            if not extractor.__class__.__name__.endswith('Extractor'):
                continue
            for request in extractor.start_url():
                self.put(request)
                self.log.info(f'project:project_id->{self.project.project_id} success send a request->{request.sign}')
                count += 1
                if count > 100:
                    self.log.warning(f'Debug url over 100 ... Ignore remaining URLs')
                    break
            break

    @property
    def project_name(self):
        return os.path.basename(os.getcwd())

    def put(self, request: Request):
        """向优先队列中存入req"""
        try:
            self.priority_queue[request.priority].put(request)
            self.log.debug(f'success send request {request}')
        except IndexError:
            ParserError(
                f'At req:%s, requests.priority=%s must between 1~%s' % (request.url, request.priority, self.max_priority))

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

    def load_module(self, cls_name):
        module_name = class_name2module_name(cls_name)
        module_type = module_name.split('_')[-1]
        if module_type == 'extractor':
            module_path = f'{os.environ[PLATFORM_NAME_ENV]}.projects.{self.project.project_name}.extractor'
        else:
            module_path = f'{os.environ[PLATFORM_NAME_ENV]}.{module_type}.{module_name}'

        try:
            mod = import_module(module_path)

            for obj in vars(mod).values():
                if inspect.isclass(obj):
                    if obj.__name__ == cls_name:
                        self.log.debug(f'success find {module_type}:{obj.__name__} from local')
                        return cls_name, mod
        except ModuleNotFoundError:
            pass

        sql = "select `content` from `{}` where `name`=%s;".format(self.frame_settings['CODE_STORE_TABLE'])
        info = self.mysql_client.select(sql, (cls_name))
        if len(info):
            self.log.debug(f'success find module:{cls_name} from remote')
            return cls_name, info[0]['content']
        else:
            raise ModuleExistError('load module from remote failed %s is not exists' % (cls_name))

# @Time    : 2019/9/27 5:37 下午
# @Author  : baii
# @File    : debuger
# @Use     : 开发时的调试模块，使用优先队列来模拟rabbitMQ
import asyncio
import inspect
import json
import os
from os.path import abspath
from queue import Queue

from bspider.config import FrameSettings
from bspider.core import ProjectConfigParser
from bspider.downloader import BaseMiddleware
from bspider.downloader.async_downloader import AsyncDownloader
from bspider.parser import BasePipeline, BaseExtractor
from bspider.parser.async_parser import AsyncParser
from bspider.http import Request
from bspider.utils.conf import PLATFORM_NAME_ENV
from bspider.utils.exceptions import ModuleExistError
from bspider.utils.importer import walk_modules, import_module_by_code
from bspider.utils.database.mysql import MysqlHandler
from bspider.utils.logger import LoggerPool
from bspider.utils.sign import Sign
from bspider.utils.tools import make_sign


class Debuger(object):
    """继承此类进行BSpider 框架的开发调试"""
    frame_settings = FrameSettings()

    # 最大下载次数 下载超过此数量个 Request 调试进程会终止
    max_follow_url_num = 10
    # 调试的url链接
    start_request = Request('http://127.0.0.1')

    # proority fix rabbitmq 数字越大优先级越高，使用Python优先队列模拟的时候需要进行优先级翻转

    def __init__(self):
        self.log = LoggerPool().get_logger(
            key=self.project_name,
            module='debuger',
            project=self.project_name,
            fn='terminal'
        )

        self.settings = ProjectConfigParser(open(abspath('settings.json')).read())
        self.__pipeline = self.settings.pipeline.copy()
        self.__middleware = self.settings.middleware.copy()
        self.settings.pipeline.clear()
        self.settings.middleware.clear()

        self.local_project_class = self.__find_local_class()
        self.mysql_handler = MysqlHandler.from_settings(self.frame_settings.get('WEB_STUDIO_DB'))
        self.max_priority = self.frame_settings['QUEUE_ARG'].get('x-max-priority', 5)
        self.priority_queue = [Queue() for _ in range(self.max_priority)]

        self.put(self.start_request)

        self.__cur_download_num = 1
        self.parser = self.parser()
        self.downloader = self.downloader()

    @property
    def project_name(self):
        return os.path.basename(os.getcwd())

    def put(self, request: Request):
        """向优先队列中存入req"""
        try:
            if request.data:
                request.sign = make_sign(self.project_name, request.url, json.dumps(request.data))
            else:
                request.sign = make_sign(self.project_name, request.url)
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
            resp = await self.downloader.download(request)
            self.__cur_download_num += 1
            if resp is not None:
                self.log.info(f'start parser url:{resp.url} status:{resp.status}')
                reqs = await self.parser.parse(resp)
                for req in reqs:
                    self.put(req)

            if self.__cur_download_num > self.max_follow_url_num:
                self.log.info(f'debuger follow url {self.max_follow_url_num} second')
                break

    def __find_local_class(self):
        # 将模块名称转换为模块代码
        local_project_class = dict()
        for mod in walk_modules(f'{os.environ[PLATFORM_NAME_ENV]}.projects.{self.project_name}'):
            for obj in vars(mod).values():
                if inspect.isclass(obj):
                    if issubclass(obj, BasePipeline) and not obj in (BasePipeline, BaseExtractor):
                        local_project_class[obj.__name__] = mod
                    if issubclass(obj, BaseMiddleware) and not obj in (BaseMiddleware,):
                        local_project_class[obj.__name__] = mod
        return local_project_class

    def load_remote_module(self, class_name):
        """加载远程代码"""
        sql = "select `content` from `%s` where `name`='%s';"
        info = self.mysql_handler.select(sql, (self.frame_settings['CODE_STORE_TABLE'], class_name))
        if len(info):
            self.log.debug(f'success find module:{class_name} from remote')
            return import_module_by_code(class_name, info[0]['content'])
        else:
            raise ModuleExistError(f'module:{class_name} is not exists')

    def parser(self) -> AsyncParser:
        """修复无法debug的bug"""
        _parser = AsyncParser(self.settings, Sign())

        # 判断调用仓库代码还是本地代码
        for pipeline in self.__pipeline:
            if pipeline in self.local_project_class:
                _parser.pipes.append(
                    getattr(self.local_project_class[pipeline], pipeline)(self.settings.parser_settings, self.log))
            else:
                _parser.pipes.append(
                    getattr(self.load_remote_module(pipeline), pipeline)(self.settings.parser_settings, self.log))

        return _parser

    def downloader(self) -> AsyncDownloader:
        # 判断调用仓库代码还是本地代码
        _downloader = AsyncDownloader(self.settings, Sign())

        # 判断调用仓库代码还是本地代码
        for middleware in self.__middleware:
            if middleware in self.local_project_class:
                _downloader.mws.append(
                    getattr(self.local_project_class[middleware], middleware)(self.settings.parser_settings, self.log))
            else:
                _downloader.mws.append(
                    getattr(self.load_remote_module(middleware), middleware)(self.settings.parser_settings, self.log))

        return _downloader


if __name__ == '__main__':
    for i in range(10, 0):
        print(i)
        'ProjectConfigError'

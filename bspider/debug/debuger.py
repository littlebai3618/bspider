# @Time    : 2019/9/27 5:37 下午
# @Author  : baii
# @File    : debuger
# @Use     : 开发时的调试模块
import asyncio
import inspect
import json
import os
from os.path import abspath
from queue import Queue

from bspider.config import FrameSettings
from bspider.core.downloader import BaseMiddleware
from bspider.core.downloader.async_downloader import AsyncDownloader
from bspider.core.parser import BasePipeline, BaseExtractor
from bspider.core.parser.async_parser import AsyncParser
from bspider.http import Request
from bspider.utils.conf import PLATFORM_NAME_ENV
from bspider.utils.importer import walk_modules
from bspider.utils.database.mysql import MysqlHandler
from bspider.utils.logger import LoggerPool


class Debuger(object):
    """继承此类进行BSpider 框架的开发调试"""
    frame_settings = FrameSettings()

    # 最大下载次数 下载超过此数量个 Request 调试进程会终止
    max_follow_url_num = 10
    # 调试的url链接
    debug_request = Request('http://127.0.0.1')

    def __init__(self):
        self.log = LoggerPool().get_logger(key=self.project_name, module='debuger',
                                           project=self.project_name)

        try:
            self.settings = json.load(open(abspath('settings.json')))
        except Exception:
            self.log.error(f'Can\'t found {self.project_name} settings!')
            return

        self.local_project_class = self.__find_local_class()
        self.mysql_handler = MysqlHandler.from_settings(self.frame_settings.get('WEB_STUDIO_DB'))

        self.queue: Queue[Request] = Queue()
        self.queue.put(self.debug_request)
        self.__cur_download_num = 1
        self.parser = self.parser()
        self.downloader = self.downloader()

    @property
    def project_name(self):
        return os.path.basename(os.getcwd())

    def start(self):
        """开始调试"""
        tasks = [asyncio.ensure_future(self.__debug())]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

        self.log.info('debuger finished')

    def set_debug_request(self, request: Request):
        self.queue.put(request)

    async def __debug(self):
        while True:
            if self.queue.empty():
                self.log.debug('candidate queue is empty')
                break

            request = self.queue.get()
            self.log.info(f'start download url:{request.url}')
            resp = await self.downloader.download(request)
            self.__cur_download_num += 1
            if resp is not None:
                self.log.info(f'start parser url:{resp.url} status:{resp.status}')
                reqs = await self.parser.parse(resp)
                for req in reqs:
                    self.queue.put(req)

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
                        local_project_class[obj.__name__] = mod.__file__
                    if issubclass(obj, BaseMiddleware) and not obj in (BaseMiddleware, ):
                        local_project_class[obj.__name__] = mod.__file__
        return local_project_class

    def load_remote_module_str(self, class_name):
        """加载远程代码"""
        sql = "select `content` from `%s` where `name`='%s';"
        info = self.mysql_handler.select(sql, (self.frame_settings['CODE_STORE_TABLE'], class_name))
        if len(info):
            self.log.debug(f'success find module:{class_name} from remote')
            return info[0]['content']
        else:
            self.log.warning(f'module:{class_name} is not exists in remote')
            return ''

    def load_local_module_str(self, class_name):
        with open(self.local_project_class[class_name], 'r') as f:
            return f.read()

    def parser(self) -> AsyncParser:
        # 判断调用仓库代码还是本地代码
        pipelines = self.settings['parser_config']['pipeline']
        for i, pipeline in enumerate(pipelines):
            if pipeline in self.local_project_class:
                self.settings['parser_config']['pipeline'][i] = (pipeline, self.load_local_module_str(pipeline))
            else:
                self.settings['parser_config']['pipeline'][i] = (pipeline, self.load_remote_module_str(pipeline))

        return AsyncParser(self.project_name, self.settings['parser_config'], 'debug')

    def downloader(self) -> AsyncDownloader:
        # 判断调用仓库代码还是本地代码
        pipelines = self.settings['downloader_config']['middleware']
        for i, pipeline in enumerate(pipelines):
            if pipeline in self.local_project_class:
                self.settings['downloader_config']['middleware'][i] = (pipeline, self.load_local_module_str(pipeline))
            else:
                self.settings['downloader_config']['middleware'][i] = (pipeline, self.load_remote_module_str(pipeline))

        return AsyncDownloader(self.project_name, self.settings['downloader_config'], 'debug')

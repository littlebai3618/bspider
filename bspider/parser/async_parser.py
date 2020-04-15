"""
2019-08-29 增加callback 参数处理 - 需要单独抽象出extractor类
将Request 对象发送到待下载队列
2020-03-18 增加SendRequestHelper
"""
from types import GeneratorType

from bspider.core import Project
from bspider.http import Response, Request
from bspider.utils.exceptions import ParserError
from bspider.utils.logger import LoggerPool
from bspider.utils.importer import import_module_by_code
from bspider.utils.sign import Sign


class SendRequestHelper(object):

    def process_item(self, item):
        if isinstance(item, Request):
            yield item

    async def _exec(self, func_name, *args):
        return getattr(self, func_name)(*args)


class AsyncParser(object):

    def __init__(self, project: Project, sign: Sign, log_fn: str):
        """传入下载器的配置文件"""
        self.sign = sign
        self.project_name = project.project_name
        self.project_id = project.project_id

        self.log = LoggerPool().get_logger(
            key=f'project_parser->{self.project_id}', fn=log_fn, module='parser', project=self.project_name)

        self.pipes = []
        for pipeline in project.parser_settings.pipeline:
            for cls, params in pipeline.items():
                cls_name, code = cls
                if isinstance(code, str):
                    mod = import_module_by_code(cls_name, code)
                else:
                    mod = code
                if mod:
                    if hasattr(mod, cls_name):
                        try:
                            self.pipes.append(
                                getattr(mod, cls_name)(project, {**project.global_settings, **params}, self.log))
                            self.log.info(f'success load: <{self.project_name}:{cls_name}>!')
                        except Exception as e:
                            raise ParserError(
                                '%s pipeline init failed: %s like: %s' % (self.project_name, cls_name, e))
                else:
                    msg = f'{self.project_name} pipeline init failed: {cls_name}'
                    raise ParserError(msg)
        # 增加默认的 SendRequestHelper
        self.pipes.append(SendRequestHelper())

    async def parse(self, response: Response) -> list:
        """
        :param response:
        :return:
        """
        all_items = [response]
        requests = []

        for index, pipeline in enumerate(self.pipes):
            cur_items = []
            for item in all_items:
                await self.__get_items(pipeline, item, cur_items, requests)
            all_items = cur_items

        return requests

    async def __get_items(self, pipeline, pre_item, cur_item, requests):
        """
        得到产生的item
        :param pipeline: 当前 pipline 对象
        :param pre_item: 上一个 pipline 产生的item
        :param cur_item: 这个 pipline 产生的item
        :return:
        """
        self.log.debug(f'{pipeline.__class__.__name__} executing process_response')
        temp_items = await pipeline._exec('process_item', pre_item)
        is_send_request_helper = isinstance(pipeline, SendRequestHelper)
        self.__exec_items(temp_items, requests, cur_item, is_send_request_helper)

    def __exec_items(self, items, requests: list, cur_item: list, is_send_request_helper: bool):
        if not isinstance(items, GeneratorType):
            if isinstance(items, Request):
                if is_send_request_helper:
                    requests.append(items)
            cur_item.append(items)
            return

        while True:
            try:
                self.__exec_items(next(items), requests, cur_item, is_send_request_helper)
            except StopIteration as e:
                self.__exec_items(e.value, requests, cur_item, is_send_request_helper)
                break

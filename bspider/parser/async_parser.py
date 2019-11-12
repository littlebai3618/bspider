# @Time    : 2019/7/9 2:29 PM
# @Author  : 白尚林
# @File    : async_parser
# @Use     :
"""初始化解析器类 加上异步mysql 的处理
   2019-08-29 增加callback 参数处理 - 需要单独抽象出extractor类
   将Request 对象发送到待下载队列
"""
from types import GeneratorType

from bspider.core import ProjectConfigParser
from bspider.http import Response, Request
from bspider.utils.exceptions import ParserError
from bspider.utils.logger import LoggerPool
from bspider.utils.importer import import_module_by_code
from bspider.utils.sign import Sign


class AsyncParser(object):

    def __init__(self, config: ProjectConfigParser, sign: Sign, log_fn: str):
        """传入下载器的配置文件"""
        self.sign = sign
        self.project_name = config.project_name
        self.project_id = config.project_id

        self.log = LoggerPool().get_logger(key=f'project_parser->{self.project_id}', fn=log_fn, module='parser', project=self.project_name)

        self.pipes = []
        for cls_name, code in config.pipeline:
            mod = import_module_by_code(cls_name, code)
            self.log.info(f'success load: <{self.project_name}:{cls_name}>!')
            if mod:
                if hasattr(mod, cls_name):
                    try:
                        # 通过中间件类名实例化，放入中间件list中
                        self.pipes.append(getattr(mod, cls_name)(config.parser_settings, self.log))
                    except Exception as e:
                        raise ParserError(f'{self.project_name} pipeline init failed: {cls_name} like: {e}')
            else:
                msg = f'{self.project_name} pipeline init failed: {cls_name}'
                raise ParserError(msg)


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
        self.__exec_items(temp_items, requests, cur_item)


    def __exec_items(self, items, requests: list, cur_item: list):
        if not isinstance(items, GeneratorType):
            if isinstance(items, Request):
                requests.append(items)
            else:
                cur_item.append(items)
            return

        while True:
            try:
                self.__exec_items(next(items), requests, cur_item)
            except StopIteration as e:
                self.__exec_items(e.value, requests, cur_item)
                break











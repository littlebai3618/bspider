# @Time    : 2019/7/9 2:29 PM
# @Author  : 白尚林
# @File    : async_parser
# @Use     :
"""初始化解析器类 加上异步mysql 的处理
   2019-08-29 增加callback 参数处理 - 需要单独抽象出extractor类
   将Request 对象发送到待下载队列
"""
from types import GeneratorType

from bspider.core import ProjectConfigParser, Sign
from bspider.http import Response, Request
from bspider.utils.exceptions import ParserError
from bspider.utils.logger import LoggerPool
from bspider.utils.importer import import_module_by_code


class AsyncParser(object):

    def __init__(self, project_name: str, config: ProjectConfigParser, sign: Sign):
        """传入下载器的配置文件"""
        self.sign = sign
        self.log = LoggerPool().get_logger(key=project_name, module='parser', project=project_name)
        self.pipes = []
        self.project_name = project_name
        for cls_name, code in config.pipeline:
            mod = import_module_by_code(cls_name, code)
            self.log.info(f'success load: <{project_name}:{cls_name}>!')
            if mod:
                if hasattr(mod, cls_name):
                    try:
                        # 通过中间件类名实例化，放入中间件list中
                        mw_instance = getattr(mod, cls_name)(config.parser_settings, self.log)
                        self.pipes.append(mw_instance)
                    except Exception as e:
                        raise ParserError(f'{project_name} pipline init failed: {cls_name} like: {e}')
            else:
                msg = f'{project_name} pipeline init failed: {cls_name}'
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
        # 处理生成器类型
        if isinstance(temp_items, GeneratorType):
            while True:
                try:
                    result = next(temp_items)
                    if result:
                        if isinstance(result, Request):
                            requests.append(result)
                        else:
                            cur_item.append(result)
                except StopIteration as e:
                    if e.value:
                        if isinstance(e.value, Request):
                            requests.append(e.value)
                        else:
                            cur_item.append(e.value)
                    break
        else:
            if temp_items:
                if isinstance(temp_items, Request):
                    requests.append(temp_items)
                else:
                    cur_item.append(temp_items)

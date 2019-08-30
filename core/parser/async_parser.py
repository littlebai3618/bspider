# @Time    : 2019/7/9 2:29 PM
# @Author  : 白尚林
# @File    : async_parser
# @Use     :
"""初始化解析器类 加上异步mysql 的处理
   2019-08-29 增加callback 参数处理 - 需要单独抽象出extractor类
   将Request 对象发送到待下载队列
"""
from types import GeneratorType

from core.lib.http import Response, Request
from util.exceptions.exceptions import ParserError
from util.logger import log_pool
from util.moduler import ModuleImporter


class AsyncParser(object):

    def __init__(self, project_name, config, sign):
        """传入下载器的配置文件"""
        self.sign = sign
        self.log = log_pool.get_logger(key=project_name, level='INFO', module='parser', project=project_name)
        pipes = config['pipeline']
        settings = config['settings']
        self.pipes = []
        self.project_name = project_name
        for cls_name, code in pipes:
            mod = ModuleImporter.import_module(cls_name, code, project_name)
            if mod:
                if hasattr(mod, cls_name):
                    try:
                        # 通过中间件类名实例化，放入中间件list中
                        mw_instance = getattr(mod, cls_name)(settings, self.log)
                        self.pipes.append(mw_instance)
                    except Exception as e:
                        raise ParserError(f'{project_name} pipline init failed: {cls_name} like: {e}')
            else:
                msg = f'{project_name} pipeline init failed: {cls_name}'
                raise ParserError(msg)

    async def parse(self, response: Response):
        """
        :param response:
        :return:
        """
        all_items = [response]
        requests = []

        for index, pipeline in enumerate(self.pipes):
            cur_items = []
            for item in all_items:
                self.__get_items(pipeline, item, cur_items, requests)
            all_items = cur_items

        return requests

    def __get_items(self, pipeline, pre_item, cur_item, requests):
        """
        得到产生的item
        :param pipeline: 当前 pipline 对象
        :param pre_item: 上一个 pipline 产生的item
        :param cur_item: 这个 pipline 产生的item
        :return:
        """
        temp_items = pipeline.process_item(pre_item)
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

# @Time    : 2019/7/9 2:29 PM
# @Author  : 白尚林
# @File    : async_parser
# @Use     :
"""初始化解析器类 加上异步mysql 的处理"""
from types import GeneratorType

from core.lib.http import Response
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
        item = response
        all_items = []
        for index, pipline in enumerate(self.pipes):
            cur_items = []
            if index == 0:
                self.__get_items(pipline, item, cur_items)
                all_items = cur_items
            else:
                for item in all_items:
                    self.__get_items(pipline, item, cur_items)
                all_items = cur_items
        del all_items

    def __get_items(self, pipline, pre_item, cur_item):
        """
        得到产生的item
        :param pipline: 当前pipline 方法
        :param pre_item: 上一个pipline 产生的item
        :param cur_item: 这个pipline 产生的item
        :return:
        """
        temp_items = pipline.process_item(pre_item)
        if isinstance(temp_items, GeneratorType):
            while True:
                try:
                    cur_item.append(next(temp_items))
                except StopIteration as e:
                    if e.value:
                        cur_item.append(e.value)
                    break
        else:
            cur_item.append(temp_items)

# @Time    : 2019/7/8 4:31 PM
# @Author  : 白尚林
# @File    : base_middleware
# @Use     :
from logging import Logger

from bspider.core.custom_module import BaseCustomModule


class BaseMiddleware(BaseCustomModule):

    def __init__(self, settings: dict, log: Logger):
        """
        构造方法
        如果需要设置配置，由各个中间件自己重写
        :param settings:
        """
        self.settings = settings
        self.log = log

    def process_request(self, request):
        """
        执行下载前的操作
        返回Response类型，作为response完成下载，跳过后面的下载阶段，直接进入下载后的中间件
        返回空或其他返回值 继续下一个中间件
        此为协程方式也可通过常规方式调用
        def process_request(self, request)
        """
        return None


    def process_response(self, request, response):
        """
        执行下载后的操作，各个中间件进行重写
        返回Response类型，正常，继续下一个中间件
        返回None类型或其他返回值，丢弃，后面不再处理
        """
        return response

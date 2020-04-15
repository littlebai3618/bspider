from bspider.core.custom_module import BaseCustomModule
from bspider.http import Request, Response


class BaseMiddleware(BaseCustomModule):

    def process_request(self, request: Request):
        """
        执行下载前的操作
        返回Response类型，作为response完成下载，跳过后面的下载阶段，直接进入下载后的中间件
        返回空或其他返回值 继续下一个中间件
        此为协程方式也可通过常规方式调用
        def process_request(self, request)
        """
        return None


    def process_response(self, request: Request, response: Response):
        """
        执行下载后的操作，各个中间件进行重写
        返回Response类型，正常，继续下一个中间件
        返回None类型或其他返回值，丢弃，后面不再处理
        """
        return response


    def process_exception(self, request: Request, e, response: Response):
        """
        这里捕获下载时发生的异常，不包括中间件异常
        返回Response类型，正常，继续下一个中间件
        返回None类型或其他返回值，丢弃，后面不再处理
        """
        return response

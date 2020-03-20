import sys
from types import GeneratorType

from bspider.http import Response
from bspider.parser import BasePipeline
from bspider.utils.exceptions import ExtractorCallbackError


class BaseExtractor(BasePipeline):

    def start_url(self) -> list:
        """生成任务起始的URL"""
        raise NotImplementedError

    def process_item(self, response):
        if isinstance(response, Response):
            if response.callback:
                try:
                    items = getattr(self, response.callback)(response)
                    if not isinstance(items, GeneratorType):
                        return items

                    for item in items:
                        yield item
                except Exception as e:
                    tp, msg, tb = sys.exc_info()
                    e.with_traceback(tb)
                    yield getattr(self, response.errback)(response, e, msg)
            else:
                raise ExtractorCallbackError('Cannot find callback %s in extractor %s' %
                                             (self.__class__.__name__, response.callback))
        yield response

    def parser(self, response: Response):
        """
        此方法需要被重构
        当一个 response 对象没有指定 callback 方法时此方法将被执行
        """
        pass

    def errback(self, response: Response, e: Exception, traceback: str):
        raise e

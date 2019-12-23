"""
extractor 方法 如果传入Response 匹配到callback 那么执行self.callback 否则 抛出异常
extractor 也是Pipeline中的一种，通过执行Response 中的callback方法返回item
"""
from bspider.http import Response
from bspider.parser import BasePipeline
from bspider.utils.exceptions import ExtractorCallbackError


class BaseExtractor(BasePipeline):

    def process_item(self, response):
        if isinstance(response, Response):
            if hasattr(self, response.callback):
                try:
                    yield getattr(self, response.callback)(response)
                except Exception as e:
                    if response.errback and hasattr(self, response.errback):
                        yield getattr(self, response.errback)(response, e)
                    raise e
            else:
                raise ExtractorCallbackError('Cannot find callback %s in extractor %s' %
                                             (self.__class__.__name__, response.callback))
        yield response

    def parser(self, response: Response):
        """
        此方法需要被重构
        当一个respons对象没有指定callback方法时此方法将被执行
        """
        pass

    def exception(self, response: Response, e: Exception):
        """
        此方法不一定需要重构
        只是提供一个demo
        ***一个extractor 可以有多个errback方法和 callback方法
        """
        raise e

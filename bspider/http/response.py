"""
这里着重参考了scrapy 的response 对象
Response 对象要求实现domps 和 loads 方法来完成 obj <-> 消息之间的转换
"""
import copy
import json

from lxml import etree

from bspider.http import Request
from bspider.http.base_http import BaseHttp


class Response(BaseHttp):
    def __init__(self,
                 url,
                 status,
                 request,
                 headers=None,
                 cookies=None,
                 text=None):
        self.url = self._set_url(url)
        self.headers = self._set_headers(headers)
        self.status = status
        self.text = self._set_text(text)
        self.cookies = self._set_cookies(cookies)
        self.request = self.__set_request(request)
        self.callback = self.request.callback
        self.errback = self.request.errback
        self.sign = self.request.sign
        self.meta = self.request.meta
        self.method = self.request.method

    def __set_request(self, request):
        if isinstance(request, dict):
            return Request.loads(request)
        elif isinstance(request, Request):
            return request
        else:
            raise TypeError("%s request must be dict or bspider.Request object. " % (type(self).__name__))

    def dumps(self):
        """解决序列化的嵌套问题"""
        resp = dict(
            url=self.url,
            status=self.status,
            request=self.request if not isinstance(self.request, Request) else self.request.dumps(),
            headers=self.headers,
            cookies=self.cookies,
            text=self.text
        )
        return resp

    @classmethod
    def loads(cls, param: dict):

        return cls(**param)

    @property
    def json(self):
        return json.loads(self.text)

    @property
    def xpath_selector(self):
        """:return a xpath selector obj"""
        return etree.HTML(self.text)

    def __str__(self):
        return "<Response:%s %s %s>" % (self.method, self.status, self.url)

    __repr__ = __str__

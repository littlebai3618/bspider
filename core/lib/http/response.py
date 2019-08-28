# @Time    : 2019/6/12 2:25 PM
# @Author  : 白尚林
# @File    : response
# @Use     :
"""
这里着重参考了scrapy 的response 对象
相比flanker 的单薄对象新加入callback, errback 两种属性

Response 对象要求实现domps 和 loads 方法来进行 obj <-> 消息之间的转换
"""
import copy
import json

from core.lib.http import Request
from core.lib.http.base_http import BaseHttp


class Response(BaseHttp):
    """
    自建response类型,仿照scrapy的response
    暂时只是存放一些属性
    """
    def __init__(self,
                 url,
                 status,
                 sign='',
                 headers=None,
                 cookies=None,
                 text=None,
                 request=None,
                 meta=None,
                 method='GET'):
        self.url = self._set_url(url)
        self.headers = self._set_headers(headers)
        self.status = status
        self.text = self._set_text(text)
        self.cookies = self._set_cookies(cookies)
        self.sign = sign
        if isinstance(request, dict):
            self.request = Request.loads(request)
        else:
            self.request = None
        self.meta = meta or {}
        self.method = method

    def dumps(self):
        """解决序列化的嵌套问题"""
        resp = copy.copy(self.__dict__)
        if isinstance(resp['request'], Request):
            resp['request'] = resp['request'].dumps()
        return resp

    @classmethod
    def loads(cls, param: dict):
        return cls(**param)


if __name__ == '__main__':
    mm = Request.loads({
        'url': 'zzzz',
        'headers': {},
        'cookies': {},
        'method': 'POST',
        'data': {},
        'meta': {},
        'priority': 2,
        'sign': 'z',
        'proxy': 'z',  # 下载是否需要使用代理
        'allow_redirect': False,  # 下载是否需要重定向
        'timeout': 20,
        'verify_ssl': False
    })

    cc = Response.loads({
        'url': 'zzz',
        'status': 200,
        'request': mm
    })
    print(cc.request)

    print(cc.dumps())

    print(cc.request)

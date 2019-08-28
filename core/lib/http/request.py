# @Time    : 2019/6/12 4:23 PM
# @Author  : 白尚林
# @File    : request
# @Use     :
"""
集成callback errback 方法的request
"""
import json

from core.lib.http.base_http import BaseHttp


class Request(BaseHttp):

    def __init__(self,
                 url,
                 method='GET',
                 headers=None,
                 data=None,
                 cookies=None,
                 meta=None,
                 priority=3,
                 sign='',
                 proxy=None,
                 allow_redirect=False,
                 timeout=10,
                 verify_ssl=False):
        """去掉了scrapy中的不必要的属性, 去掉了私有属性"""
        self.url = self._set_url(url)
        self.headers = self._set_headers(headers)
        self.cookies = self._set_cookies(cookies)
        self.method = self._set_method(method)
        self.data = data or {}
        self.meta = self._set_meta(meta)
        self.priority = priority
        self.sign = sign
        self.proxy = proxy # 下载是否需要使用代理
        self.allow_redirect = allow_redirect # 下载是否需要重定向
        self.timeout = timeout
        self.verify_ssl = verify_ssl

    @classmethod
    def loads(cls, param: dict):
        return cls(**param)

    def dumps(self):
        return self.__dict__

    def __str__(self):
        return "<Request:%s %s>" % (self.method, self.url)

    __repr__ = __str__

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
            'proxy': 'z', # 下载是否需要使用代理
            'allow_redirect': False, # 下载是否需要重定向
            'timeout': 20,
            'verify_ssl': False
        })

    print(json.dumps(mm))

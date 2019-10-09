# @Time    : 2019/6/12 4:23 PM
# @Author  : 白尚林
# @File    : request
# @Use     :
"""
集成callback errback 方法的request
"""
import json

from .base_http import BaseHttp


class Request(BaseHttp):

    def __init__(self,
                 url,
                 method='GET',
                 callback='parser',
                 headers=None,
                 data=None,
                 cookies=None,
                 meta=None,
                 priority: int=3,
                 sign='',
                 proxy=None,
                 allow_redirect: bool=False,
                 timeout: int=10,
                 verify_ssl: bool=False,
                 errback=None):
        """

        :param url: 需要请求的链接
        :param method: 请求的方法
        :param callback: Extractor的回调方法
        :param headers: 请求头
        :param data: HTTP请求的body参数
        :param cookies: 需要携带的cookie
        :param meta: 元数据，不跟随request发送到服务端
        :param priority: request的优先级
        :param sign: 每个请求的唯一标识，用于debug
        :param proxy: 请求携带的代理 http://proxy_ip:port
        :param allow_redirect: 是否重定向
        :param timeout: 超时时间
        :param verify_ssl: 是否校验证书
        :param errback: 解析异常时的回调函数
        """
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
        self.callback = self._set_callback(callback)
        self.errback = self._set_errback(errback)

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

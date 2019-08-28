# @Time    : 2019/6/12 5:21 PM
# @Author  : 白尚林
# @File    : base_http
# @Use     :


class BaseHttp(object):


    # SET ATTR METHOD _set_{attr_name}
    req_attr = {'url', 'headers', 'cookies', 'method', 'data', 'meta', 'priority', 'sign', 'proxy', 'allow_redirect', 'timeout', 'verify_ssl'}

    def _set_url(self, url):
        if isinstance(url, str):
            return url
        else:
            raise TypeError('{} url must be str, got: {}'.format(type(self).__name__, type(url).__name__))

    def _set_headers(self, headers):
        if headers is None:
            return {}
        elif not isinstance(headers, dict):
            raise TypeError("{} headers must be dict. ".format(type(self).__name__))
        else:
            return headers

    def _set_cookies(self, cookies):
        if cookies is None:
            return
        elif not isinstance(cookies, dict):
            raise TypeError("{} cookies must be dict or None. ".format(type(self).__name__))
        else:
            return cookies

    def _set_method(self, method):
        if method is None:
            return 'GET'
        if isinstance(method, str):
            method = method.upper()
            if method in 'GET, POST, PUT ,PATCH, OPTIONS, HEAD, DELETE':
                return method
            else:
                raise TypeError("{} method: {} is not support. ".format(type(self).__name__, method))

        raise TypeError("{} method must be str. ".format(type(self).__name__))

    def _set_meta(self, meta):
        if meta is None:
            return {}
        elif not isinstance(meta, dict):
            raise TypeError("{} meta must be dict or None. ".format(type(self).__name__))
        else:
            return meta

    def _set_data(self, data):
        if data is None:
            return
        elif not isinstance(data, dict):
            raise TypeError("{} data must be dict or None. ".format(type(self).__name__))
        else:
            return data

    def __set_priority(self, priority):
        if priority is None:
            return
        elif isinstance(priority, int):
            return priority
        raise TypeError("{} priority must be int. ".format(type(self).__name__))

    def __set_allow_redirect(self, allow_redirect):
        """默认禁止重定向"""
        if isinstance(allow_redirect, bool):
            return allow_redirect
        return False

    def __set_timeout(self, timeout):
        """默认时间是20秒"""
        if isinstance(timeout, int):
            return timeout
        return 20

    def __set_verify_ssl(self, verify_ssl):
        if isinstance(verify_ssl, bool):
            return verify_ssl
        return False


    # Response API
    def _set_text(self, text):
        if text is None:
            return ''
        elif not isinstance(text, str):
            raise TypeError("{} text must be str. ".format(type(self).__name__))
        else:
            return text
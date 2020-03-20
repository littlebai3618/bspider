class BaseHttp(object):

    def _set_url(self, url):
        if isinstance(url, str):
            return url
        else:
            raise TypeError('%s url must be str, got: %s' % (type(self).__name__, type(url).__name__))

    def _set_headers(self, headers):
        if headers is None:
            return dict()
        elif not isinstance(headers, dict):
            raise TypeError("%s headers must be dict. " % (type(self).__name__))
        else:
            return headers

    def _set_cookies(self, cookies):
        if cookies is None:
            return
        elif not isinstance(cookies, dict):
            raise TypeError("%s cookies must be dict or None. " % (type(self).__name__))
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
                raise TypeError("%s method: %s is not support. " % (type(self).__name__, method))

        raise TypeError("%s method must be str. " % (type(self).__name__))

    def _set_meta(self, meta):
        if meta is None:
            return dict()
        elif not isinstance(meta, dict):
            raise TypeError("%s meta must be dict or None. " % (type(self).__name__))
        else:
            return meta

    def _set_data(self, data):
        if data is None:
            return
        elif not isinstance(data, dict):
            raise TypeError("%s data must be dict or None. " % (type(self).__name__))
        else:
            return data

    def _set_params(self, params):
        if params is None:
            return
        elif not isinstance(params, dict):
            raise TypeError("%s params must be dict or None. " % (type(self).__name__))
        else:
            return params

    # Response API
    def _set_text(self, text):
        if text is None:
            return ''
        elif not isinstance(text, str):
            raise TypeError("%s text must be str. " % (type(self).__name__))
        else:
            return text

    def _set_callback(self, callback):
        if callable(callback):
            return callback.__name__
        elif isinstance(callback, str):
            return callback
        else:
            raise TypeError('callback must be callable or str')

    def _set_errback(self, errback):
        if callable(errback):
            return errback.__name__
        elif isinstance(errback, str) or errback is None:
            return errback
        else:
            raise TypeError('error callback must be callable or str')

    def _set_proxy(self, proxy):
        if proxy is None:
            return
        elif not isinstance(proxy, dict):
            raise TypeError("%s proxy must be dict or None. " % (type(self).__name__))
        elif 'proxy' not in proxy:
            raise KeyError("%s proxy must have key:\'proxy\'. " % (type(self).__name__))
        else:
            return proxy

# @Time    : 2019/10/30 7:17 下午
# @Author  : baii
# @File    : sign
# @Use     : 标志位，标志下载器解析器等对象是否需要更新
import hashlib
import json


class Sign(object):

    def __init__(self, **kwargs):
        plaintext = json.dumps(kwargs).encode('utf-8')
        self.__sign = hashlib.md5(plaintext).hexdigest()

    def __eq__(self, other):
        return self.__sign == str(other)

    def __str__(self):
        return self.__sign

# @Time    : 2021/5/12 下午6:26
# @Author  : baii
# @File    : TupleC
# @Use     :
from typing import Any


class TupleC(object):

    def __init__(self, cls: Any, params: dict):
        self.cls = cls
        self.params = params

    def __iter__(self):
        self.is_iter = True
        return self

    def __next__(self):
        if self.is_iter:
            self.is_iter = False
            return self

        raise StopIteration()

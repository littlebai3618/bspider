# @Time    : 2021/5/12 下午6:26
# @Author  : baii
# @File    : TupleC
# @Use     :
from typing import Any


class TupleC(object):

    def __init__(self, cls: Any, params: dict):
        self.cls = cls
        self.params = params
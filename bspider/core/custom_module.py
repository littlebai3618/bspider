import logging
from asyncio import iscoroutinefunction

from bspider.core import Project


class BaseCustomModule(object):

    def __init__(self, project: Project, settings: dict, log: logging.Logger):
        """
        构造函数，提供当前project对象，和当前模块的
        :param project: project对象
        :param settings: 当前模块的参数
        :param log: 日志句柄
        """
        self.project = project
        self.settings = settings
        self.log = log

    async def _exec(self, func_name, *args):
        """用以支持协程和非协程编程方式"""
        func = getattr(self, func_name)
        if iscoroutinefunction(func):
            return await func(*args)
        else:
            return func(*args)
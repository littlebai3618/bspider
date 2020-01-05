import logging

from bspider.config import FrameSettings
from bspider.utils.exceptions import MethodError


class BaseOperation(object):

    def __init__(self, log: logging.Logger):
        self.frame_settings = FrameSettings()
        self.log = log


    def execute_task(self):
        raise MethodError('you must rebuild execute_task()')

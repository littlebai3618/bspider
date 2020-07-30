import logging

from bspider.config import FrameSettings


class BaseOperation(object):

    def __init__(self, log: logging.Logger):
        self.frame_settings = FrameSettings()
        self.log = log


    def execute_task(self):
        raise NotImplementedError

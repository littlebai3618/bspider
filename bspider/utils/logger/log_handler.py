import logging
import os
import sys
import re
from logging.handlers import TimedRotatingFileHandler

from bspider.utils import singleton
from bspider.config import FrameSettings
from bspider.utils.conf import PLATFORM_PATH_ENV
from bspider.utils.sign import Sign

from .formatter import get_stream_formatter, get_file_formatter


@singleton
class LoggerPool(object):
    """日志句柄池"""

    def __init__(self):
        self.__pool = {}
        self.frame_settings = FrameSettings()
        if self.frame_settings['GLOBAL_PATTERN'] == 'produce':
            self.__handle_func = self.__set_file_handler
        else:
            self.__handle_func = self.__set_stream_handler

    def __set_stream_handler(self, log, level='DEBUG', **kwargs):
        log_handler = logging.StreamHandler(stream=sys.stderr)
        log_handler.suffix = "%Y%m%d"
        log_handler.extMatch = re.compile(r"^\d{4}\d{2}\d{2}$")
        log_formatter = get_stream_formatter(**kwargs)
        log_handler.setFormatter(log_formatter)
        log.addHandler(log_handler)
        if level == 'INFO':
            log.setLevel(logging.INFO)
        elif level == 'WARNING':
            log.setLevel(logging.WARNING)
        elif level == 'DEBUG':
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        return log

    def __set_file_handler(self, log, fn, level='INFO', **kwargs):
        log_path = os.path.join(os.environ[PLATFORM_PATH_ENV], 'log', f'{fn}.log')
        log_handler = TimedRotatingFileHandler(log_path, when="midnight", backupCount=10)
        log_handler.suffix = "%Y%m%d"
        log_formatter = get_file_formatter(**kwargs)
        log_handler.setFormatter(log_formatter)
        log.addHandler(log_handler)
        if level == 'INFO':
            log.setLevel(logging.INFO)
        elif level == 'WARNING':
            log.setLevel(logging.WARNING)
        elif level == 'DEBUG':
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        return log

    def get_logger(self, key, fn, **kwargs) -> logging.Logger:
        """如果是downloader、parser模块控制终端输出到指定log文件"""
        cur_sign = Sign(**kwargs)
        if key not in self.__pool:
            log_handler = self.__handle_func(
                log=logging.getLogger(key),
                fn=fn,
                level=self.frame_settings['LOGGER_LEVEL'],
                **kwargs)
            self.__pool[key] = (cur_sign, log_handler)
            return log_handler

        pre_sign, log_handler = self.__pool[key]
        if pre_sign == cur_sign:
            return log_handler
        else:
            for handler in log_handler.handlers:
                handler.close()
                log_handler.removeHandler(handler)

            log_handler = self.__handle_func(
                log=logging.getLogger(key),
                fn=fn,
                level=self.frame_settings['LOGGER_LEVEL'],
                **kwargs)

            self.__pool[key] = (cur_sign, log_handler)
            return log_handler

        # if kwargs.get('module') in ('parser', 'downloader'):
        #     log_handler = self.__set_file_handler(logging.getLogger(unique_key), self.frame_settings['LOGGER_LEVEL'], key=key,
        #                                           **kwargs)
        # else:

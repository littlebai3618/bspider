# @Time    : 2019/7/11 3:58 PM
# @Author  : 白尚林
# @File    : log_handler
# @Use     :
import logging
import os
import sys
import re
from logging.handlers import TimedRotatingFileHandler

from bspider.config import FrameSettings
from bspider.utils.conf import PLATFORM_PATH_ENV
from bspider.utils.logger.formatter import get_stream_formatter
from bspider.utils import singleton


class RabbitMQLogHandler(logging.Handler):

    def __init__(self, mq_handler, level='INFO'):
        super().__init__(level=level)
        self.mq_handler = mq_handler
        # 创建交换机
        self.frame_settings = FrameSettings()
        self.mq_handler.declare_exchange(self.frame_settings['LOGGER_EXCHANGE_NAME'])

    def emit(self, record):
        self.mq_handler.send_message(
            exchange=self.frame_settings['LOGGER_EXCHANGE_NAME'],
            routing_key=self.frame_settings['LOGGER_EXCHANGE_NAME'],
            body=self.format(record)
        )

    def close(self):
        """
        clear when closing
        """
        logging.Handler.close(self)


@singleton
class LoggerPool(object):
    """日志句柄池"""

    def __init__(self):
        self.__pool = {}
        self.frame_settings = FrameSettings()
        if self.frame_settings['GLOBAL_PATTERN'] == 'produce':
            self.__handle_func = self.__set_rabbitmq_handler
        else:
            self.__handle_func = self.__set_stream_handler

    def __set_rabbitmq_handler(self, log, level='DEBUG', **kwargs):
        # log_handler = RabbitMQLogHandler(mq_handler=self.mq_handler)
        # log_handler.suffix = "%Y%m%d"
        # log_formatter = get_json_formatter(**kwargs)
        # log_handler.setFormatter(log_formatter)
        #
        # log.addHandler(log_handler)
        # if level == 'INFO':
        #     log.setLevel(logging.INFO)
        # elif level == 'WARNING':
        #     log.setLevel(logging.WARNING)
        # elif level == 'DEBUG':
        #     log.setLevel(logging.DEBUG)
        # else:
        #     log.setLevel(logging.INFO)
        # return log
        return self.__set_stream_handler(log, level=level, **kwargs)

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

    def __set_file_handler(self, log, level='INFO', key='default_work', **kwargs):
        log_path = os.path.join(os.environ[PLATFORM_PATH_ENV], 'log', f'{key}.log')
        log_handler = TimedRotatingFileHandler(log_path, when="midnight", backupCount=10)
        log_handler.suffix = "%Y%m%d"
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

    def get_logger(self, key, **kwargs) -> logging.Logger:
        """如果是downloader、parser模块控制终端输出到指定log文件"""
        unique_key = '{}:{}:{}'.format(key, kwargs.get('module', ''), kwargs.get('project', ''))
        if unique_key in self.__pool:
            return self.__pool[unique_key]
        if kwargs.get('module') in ('parser', 'downloader'):
            log_handler = self.__set_file_handler(logging.getLogger(unique_key), self.frame_settings['LOGGER_LEVEL'], key=key,
                                                  **kwargs)
        else:
            log_handler = self.__handle_func(logging.getLogger(unique_key), self.frame_settings['LOGGER_LEVEL'], **kwargs)
        self.__pool[unique_key] = log_handler
        return log_handler

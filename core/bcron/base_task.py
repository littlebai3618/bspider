# @Time    : 2019/7/8 3:29 PM
# @Author  : 白尚林
# @File    : base_task
# @Use     :
"""定时任务的基础类，所有定时任务类必须继承"""
import json

from core.lib import EXCHANGE_NAME
from core.lib.http import Request
from util.exceptions.exceptions import MethordError
from util.logger import log_pool
from util.rabbitMQ import RabbitMQHandler
from util.tools import make_sign
from config import frame_settings


class BaseTask(object):

    def __init__(self, settings, job_name):
        """"""
        self.settings = settings
        self.job_name = job_name
        self.log = log_pool.get_logger(key=job_name, level='INFO', module='bcorn', project=job_name)
        self.__mq_handler = RabbitMQHandler(frame_settings.RABBITMQ_CONFIG)

    def execute_task(self):
        raise MethordError('you must rebuild execute_task()')

    # Public API

    def send_request(self, request: Request):
        """发送request 到待下载队列"""
        # 逐条发送到待队列
        if request.method == 'POST':
            request.sign = make_sign(self.job_name, request.url, json.dumps(request.data))
        else:
            request.sign = make_sign(self.job_name, request.url)
        self.__set_request(request, self.job_name)

    def __set_request(self, request: Request, job_name):
        # 这里dump方法使用了浅拷贝，会影响一部分性能
        data = json.dumps(request.dumps())
        self.__mq_handler.send_msg(EXCHANGE_NAME[0], job_name, data, request.priority)
        self.log.debug(f'success set a new Request: {data}')
        return True

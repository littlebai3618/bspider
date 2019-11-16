# @Time    : 2019/7/8 3:29 PM
# @Author  : 白尚林
# @File    : base_task
# @Use     :
"""定时任务的基础类，所有定时任务类必须继承"""
import json

from bspider.config import FrameSettings
from bspider.core import ProjectConfigParser
from bspider.core.custom_module import BaseCustomModule
from bspider.http import Request
from bspider.utils.exceptions import MethodError
from bspider.utils.logger import LoggerPool
from bspider.utils.rabbitMQ import RabbitMQHandler
from bspider.utils.tools import make_sign


class BaseTask(BaseCustomModule):

    def __init__(self, settings: ProjectConfigParser):
        self.settings = settings
        self.log = LoggerPool().get_logger(key=f'task_{self.settings.project_id}', fn='bcorn', module='bcorn',
                                           project=self.settings.project_name)
        self.frame_settings = FrameSettings()
        self.__mq_handler = RabbitMQHandler(self.frame_settings['RABBITMQ_CONFIG'])

    def execute_task(self):
        raise MethodError('you must rebuild execute_task()')

    # Public API

    def send_request(self, request: Request):
        """发送request 到待下载队列"""
        # 逐条发送到待队列
        if request.data:
            request.sign = make_sign(self.settings.project_id, request.url, json.dumps(request.data))
        else:
            request.sign = make_sign(self.settings.project_id, request.url)

        # 这里dump方法使用了浅拷贝，会影响一部分性能
        data = json.dumps(request.dumps())
        self.__mq_handler.send_msg(
            self.frame_settings['EXCHANGE_NAME'][0],
            str(self.settings.project_id),
            data,
            request.priority)
        self.log.info(f'project:project_id->{self.settings.project_id} success send a request->{request.sign}')
        self.log.debug(f'project:project_id->{self.settings.project_id} Request: {data}')
        return True

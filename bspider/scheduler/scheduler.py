# @Time    : 2019-08-06 14:54
# @Author  : 白尚林
# @File    : scheduler
# @Use     :
import datetime
import json

from bspider.config.default_settings import EXCHANGE_NAME
from bspider.http import Request
from bspider.utils.logger import LoggerPool
from bspider.utils.rabbitMQ import RabbitMQHandler
from bspider.config import FrameSettings
from bspider.utils.sign import Sign


class Scheduler(object):

    def __init__(self, project_id: int, project_name: str, rate: int, sign: Sign, log_fn: str):
        self.sign = sign
        self.project_name = project_name
        self.project_id = project_id

        self.log = LoggerPool().get_logger(key=f'scheduler->{self.project_id}', fn=log_fn, module='scheduler', project=self.project_name)

        # 上一次分钟数
        self.__pre_loop_sign = None
        self.__scheduler_count = 0
        self.__download_queue = 'download_{}'.format(self.project_id)
        self.rate = rate
        self.frame_settings = FrameSettings()
        self.__mq_handler = RabbitMQHandler(self.frame_settings['RABBITMQ_CONFIG'])

    def scheduler(self):
        now = datetime.datetime.now()
        cur_loop_sign = 'scheduler-' + now.strftime('%H%M')
        # 表示新的调度周期
        if cur_loop_sign != self.__pre_loop_sign:
            self.__pre_loop_sign = cur_loop_sign
            self.__scheduler_count = 0

        cur_slice = int(int(now.strftime('%S')) // (60 / 12) + 1)

        if self.rate < 1 or self.__is_full_queue(self.__download_queue, self.rate):
            return
        else:
            # 本次调度数量
            rate_slice = self.rate / 12

            for i in range(int(rate_slice * 1.5)):
                if int(rate_slice * cur_slice) > self.__scheduler_count:
                    if self.schedule_task():
                        self.__scheduler_count += 1
                else:
                    break

    def schedule_task(self) -> bool:
        """调度抓取任务到下载队列"""
        queue_name = '{}_{}'.format(EXCHANGE_NAME[0], self.project_id)
        msg_id, data = self.__mq_handler.recv_msg(queue_name)
        if msg_id is not None:
            request = Request.loads(json.loads(data))
            if self.__mq_handler.send_msg(EXCHANGE_NAME[1], self.project_id, data, priority=request.priority):
                self.log.info(f'send a new task success sign->{request.sign}')
                self.__mq_handler.report_acknowledgment(msg_id)
                return True
            else:
                self.__mq_handler.report_unacknowledgment(msg_id)
                self.log.warning(f'send a new task fail sign->{request.sign}')
        return False

    def __is_full_queue(self, queue_name, rate):
        """检查任务的下载队列是否阻塞"""
        msg_count = self.__mq_handler.get_queue_message_count(queue_name)
        threshold = rate // 12
        if threshold < 2:
            threshold = 1
        return msg_count > threshold

    def __repr__(self):
        return f'<AsyncScheduler->{self.project_name}:{self.sign}>'

# @Time    : 2019/7/5 2:12 PM
# @Author  : 白尚林
# @File    : async_scheduler
# @Use     :
"""暂时放弃异步任务调度"""
import datetime

from bspider.core.broker import RabbitMQBroker
from bspider.utils.logger import LoggerPool
from bspider.utils.sign import Sign
from bspider.config.default_settings import EXCHANGE_NAME


class AsyncScheduler(object):

    def __init__(self, project_id: int, project_name: str, rate: int, sign: Sign, log_fn: str):
        self.sign = sign
        self.project_name = project_name
        self.project_id = project_id

        self.log = LoggerPool().get_logger(key=f'scheduler->{self.project_id}', fn=log_fn, module='scheduler', project=self.project_name)
        self.__broker = RabbitMQBroker(self.log)

        # 上一次分钟数
        self.__pre_loop_sign = None
        self.__scheduler_count = 0
        self.__downloader_queue = f'{EXCHANGE_NAME[1]}_{self.project_id}'
        self.rate = rate

    async def scheduler(self):
        now = datetime.datetime.now()
        cur_loop_sign = 'scheduler-' + now.strftime('%H%M')
        # 表示新的调度周期
        if cur_loop_sign != self.__pre_loop_sign:
            self.__pre_loop_sign = cur_loop_sign
            self.__scheduler_count = 0
        self.log.debug(f'scheduler->{self.project_id} schedule cycle {cur_loop_sign} start!')
        cur_slice = int(int(now.strftime('%S')) // (60 / 12) + 1)
        self.log.debug(f'cur_slice: {cur_slice}')

        if self.rate < 1 or await self.__is_full_queue(self.__downloader_queue, self.rate):
            # 本次调度数量
            rate_slice = self.rate / 12
            self.log.debug(f'rate_slice: {rate_slice} real plan schedule num {int(rate_slice * 4)}')
            for i in range(int(rate_slice * 4)):
                # 获取项目本分钟内已经推送的数量,和当前时间段的需要推送量比较
                if int(rate_slice * cur_slice) > self.__scheduler_count:
                    if await self.__broker.schedule_task(self.project_id):
                        self.__scheduler_count += 1
                else:
                    break
        self.log.debug(f'scheduler->{self.project_id} schedule cycle {cur_loop_sign} finish!')


    # async def do_work(self):
    #     while True:
    #         all_queue_is_none = False
    #         now = datetime.datetime.now()
    #         hash_name = 'scheduler-' + now.strftime('%H%M')
    #         # 表示新的调度周期
    #         if hash_name != self.timer.get('hash_name', ''):
    #             self.timer.clear()
    #             self.timer['hash_name'] = hash_name
    #
    #         cur_slice = int(int(now.strftime('%S')) // (60 / 12) + 1)
    #
    #         for project_name, rate in self.monitor.projects.items():
    #             # 查看速度显示是否已过,由于按照分钟进行划分，所以速度不支持小于每分钟1次的下载速度
    #             candidate_queue = 'candidate_{}'.format(project_name)
    #             download_queue = 'download_{}'.format(project_name)
    #             if rate < 1 or await self.__is_full_queue(download_queue, rate):
    #                 continue
    #             else:
    #                 all_queue_is_none = True
    #                 # 本次调度数量
    #                 rate_slice = rate / 12
    #
    #                 for i in range(int(rate_slice * 4)):
    #                     # 获取项目本分钟内已经推送的数量,和当前时间段的需要推送量比较
    #                     if int(rate_slice * cur_slice) > int(self.timer.get(project_name, 0)):
    #                         tag, body = await self.mq_handler.pull_new_message(candidate_queue)
    #                         if tag is not None:
    #                             if await self.mq_handler.send_message('download', project_name, body):
    #                                 self.log.info(f'send a new task to request queue: project:{project_name}, body:{body}')
    #                                 await self.mq_handler.report_acknowledgment(tag)
    #                                 self.timer[project_name] = self.timer.get(project_name, 0) + 1
    #                             else:
    #                                 await self.mq_handler.report_unacknowledgment(tag)
    #                         else:
    #                             break
    #                     else:
    #                         break
    #
    #         if all_queue_is_none:
    #             await asyncio.sleep(0.5)
    #
    async def __is_full_queue(self, queue_name, rate):
        """检查任务的下载队列是否阻塞"""
        msg_count = await self.__broker.mq_handler.get_queue_message_count(queue_name)
        threshold = rate // 12
        if threshold < 2:
            threshold = 1
        return msg_count > threshold
    #
    # async def __is_empty_queue(self, queue_name):
    #     count = await self.__broker.mq_handler.get_queue_message_count(queue_name)
    #     return count == 0

    def __repr__(self):
        return f'<AsyncScheduler->{self.project_name}:{self.sign}>'

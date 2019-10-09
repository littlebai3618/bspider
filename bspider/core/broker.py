# @Time    : 2019/7/2 2:41 PM
# @Author  : 白尚林
# @File    : downloader
# @Use     :
"""
rabbitMQ 的混合类，提供rabbitMQ 推拉消息的封装
"""
import json

from bspider.config import FrameSettings
from bspider.config.default_settings import EXCHANGE_NAME
from bspider.http import Request, Response
from bspider.utils.rabbitMQ import AioRabbitMQHandler


class RabbitMQBroker(object):

    def __init__(self, log):
        self.frame_settings = FrameSettings()
        self.mq_handler = AioRabbitMQHandler.from_settings(self.frame_settings['RABBITMQ_CONFIG'])
        self.log = log
        self.log.debug('rabbitMQ broker init success')

    async def set_request(self, request: Request, project_name):
        # 这里dump方法使用了浅拷贝，会影响一部分性能
        data = json.dumps(request.dumps())
        await self.mq_handler.send_msg(data, EXCHANGE_NAME[0], project_name, request.priority)
        self.log.info(f'success set a new Request: {data}')
        return True

    async def get_request(self, project_name) -> (int, Request):
        queue_name = '{}_{}'.format(EXCHANGE_NAME[1],project_name)
        msg_id, data = await self.mq_handler.recv_msg(queue_name)
        if msg_id:
            request = Request.loads(json.loads(data))
            self.log.info(f'success get a new Request: {data}')
            return msg_id, request
        return None, None

    async def set_response(self, response: Response, project_name) -> bool:
        """将解析结果发送到不同的exchange"""
        # 这里dump方法使用了浅拷贝，会影响一部分性能
        data = json.dumps(response.dumps())
        await self.mq_handler.send_msg(data, EXCHANGE_NAME[2], project_name, response.request.priority)
        self.log.debug(f'success set a new Response: {data}')
        return True

    async def get_response(self, project_name: str) -> (int, Response):
        queue_name = '{}_{}'.format(EXCHANGE_NAME[2],project_name)
        msg_id, data = await self.mq_handler.recv_msg(queue_name)
        if msg_id:
            request = Response.loads(json.loads(data))
            self.log.debug(f'success get a new Response: {data}')
            return msg_id, request
        return None, None
    
    async def schedule_task(self, project_name: str) -> bool:
        """调度抓取任务到下载队列"""
        queue_name = '{}_{}'.format(EXCHANGE_NAME[0],project_name)
        msg_id, data = await self.mq_handler.recv_msg(queue_name)
        if msg_id is not None:
            request = Request.loads(json.loads(data))
            if await self.mq_handler.send_msg(data, EXCHANGE_NAME[1], project_name, priority=request.priority):
                self.log.info(f'send a new task to request queue: job:{project_name}, body:{data}')
                await self.mq_handler.ack(msg_id)
                return True
            else:
                await self.mq_handler.nack(msg_id)
        return False

    async def report_ack(self, msg_id):
        await self.mq_handler.ack(msg_id)

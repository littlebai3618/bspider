"""
rabbitMQ 的混合类，提供rabbitMQ 推拉消息的封装
"""
import json
import logging

from bspider.config import FrameSettings
from bspider.config.default_settings import EXCHANGE_NAME
from bspider.http import Request, Response
from bspider.utils.rabbitMQ import AioRabbitMQClient


class RabbitMQBroker(object):
    # 要使用ID作为routing_key 必须要转为字符串否则无法绑定

    def __init__(self, log: logging.Logger, max_channel_size: int):
        self.frame_settings = FrameSettings()
        self.mq_client = AioRabbitMQClient(self.frame_settings['RABBITMQ_CONFIG'], max_channel_size)
        self.log = log
        self.log.debug('rabbitMQ broker init success')

    async def set_request(self, request: Request, project_id: int) -> bool:
        # 这里dump方法使用了浅拷贝，会影响一部分性能
        data = json.dumps(request.dumps())
        await self.mq_client.send_msg(data, EXCHANGE_NAME[0], str(project_id), request.priority)
        self.log.info(f'success set a new Request: {request}')
        return True

    async def set_response(self, response: Response, project_id: int) -> bool:
        """将解析结果发送到不同的exchange"""
        # 这里dump方法使用了浅拷贝，会影响一部分性能
        data = json.dumps(response.dumps())
        await self.mq_client.send_msg(data, EXCHANGE_NAME[2], str(project_id), response.request.priority)
        self.log.debug(f'success set a new Response: {response}')
        return True
    
    async def schedule_task(self, project_id: int) -> bool:
        """调度抓取任务到下载队列"""
        self.log.debug(f'start to schedule task')
        queue_name = '{}_{}'.format(EXCHANGE_NAME[0], project_id)

        async with self.mq_client.session() as session:
            msg_id, data = await session.recv_msg(queue_name)
            if msg_id is not None:
                request = Request.loads(json.loads(data))
                if await self.mq_client.send_msg(data, EXCHANGE_NAME[1], str(project_id), priority=request.priority):
                    self.log.info(f'send a new task to request queue=> project_id:{project_id}, body:{data}')
                    session.ack(msg_id)
                    return True
                else:
                    self.log.warning(f'send a new task fail sign->{request.sign}')
                    session.nack(msg_id)
        return False

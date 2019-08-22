# @Time    : 2019/7/19 11:11 AM
# @Author  : 白尚林
# @File    : async_handler
# @Use     :
"""
    实现关闭方法
"""
import asyncio
import hashlib
import time
import typing

import aiormq

from aiormq.types import ConfirmationFrameType, DrainResult
from pamqp import specification as spec

from config.frame_settings import RABBITMQ_CONFIG
from core.lib import QUEUE_ARG
from util.rabbitMQ.async_handler.pool import Pool
from util.singleton import singleton


@singleton
class RabbitMQPoolFactory(object):
    """rabbitMQ 连接池的连接池"""
    base_url = "amqp://{username}:{password}@{host}:{port}/{virtual_host}"

    def __init__(self):
        self.__pools = dict()

    @staticmethod
    def __make_hash(mq_config: dict) -> str:
        hashstr = ','.join([f'{k}:{v}' for k, v in mq_config.items()])
        hashcode = hashlib.md5(hashstr.encode('utf8')).hexdigest()
        return hashcode

    def get_pool(self, mq_config: dict) -> Pool:
        hashcode = self.__make_hash(mq_config)
        if hashcode in self.__pools:
            return self.__pools[hashcode]
        else:
            pool = Pool(
                self.get_channel,
                Pool(self.get_connection, mq_config, max_size=1),
                max_size=3,
            )
            self.__pools[hashcode] = pool
            return pool

    async def get_connection(self, mq_config: dict) -> aiormq.Connection:
        return await aiormq.connect(self.base_url.format(**mq_config))

    @staticmethod
    async def get_channel(conn_pool: Pool) -> aiormq.Channel:
        async with conn_pool.acquire() as connection:
            return await connection.channel()


class AioRabbitMQHandler(object):

    def __init__(self, config: dict):
        self.__pool = RabbitMQPoolFactory().get_pool(mq_config=config)
        self.queue_arg = QUEUE_ARG

    @classmethod
    def from_settings(cls, settings: dict):
        """通过配置创建连接对象"""
        return cls(settings)

    async def exchange_declare(self, exchange: str = None) -> spec.Exchange.DeclareOk:
        return await self._do_query(func_name='exchange_declare',
                                    exchange=exchange,
                                    exchange_type='topic',
                                    durable=True)

    async def queue_declare(self, queue: str = '') -> spec.Queue.DeclareOk:
        return await self._do_query(func_name='queue_declare',
                                    queue=queue,
                                    durable=True,
                                    arguments=self.queue_arg)

    async def get_queue_message_count(self, queue: str):
        """
        获取队列的msg数量
        :param queue:
        :return:
        """
        result = await self.queue_declare(queue)
        return result.message_count

    async def send_msg(self, msg: str, exchange: str, routing_key: str,
                       priority: int) -> typing.Optional[ConfirmationFrameType]:
        """
        发送消息 -> 默认持久化
        :param msg:
        :param exchange: 交换机名称
        :param routing_key: 路由关键字
        :param priority: 优先级 1-5 超过5将失效
        :return:
        """
        properties = spec.Basic.Properties(delivery_mode=2, priority=priority)
        return await self._do_query(
            func_name='basic_publish',
            exchange=exchange,
            routing_key=routing_key,
            body=msg.encode(),
            properties=properties)

    async def recv_msg(self, queue: str = '', no_ack: bool = False) -> tuple:
        msg = await self._do_query(func_name='basic_get', queue=queue, no_ack=no_ack)
        if msg:
            method, properties, body, _ = msg
            if method is not None and isinstance(body, bytes):
                return method.delivery_tag, body.decode()
        return None, None

    # report ACK
    async def ack(self, delivery_tag) -> DrainResult:
        return await self._do_ack('basic_ack', delivery_tag)

    async def nack(self, delivery_tag) -> DrainResult:
        return await self._do_ack('basic_nack', delivery_tag)

    async def _do_ack(self, func_name, delivery_tag):
        async with self.__pool.acquire() as channel:
            func = getattr(channel, func_name)
            return func(delivery_tag=delivery_tag)

    async def _do_query(self, func_name, **kwargs):
        async with self.__pool.acquire() as channel:
            func = getattr(channel, func_name)
            return await func(**kwargs)


async def test():
    handler = AioRabbitMQHandler(RABBITMQ_CONFIG['manager'])
    while True:
        ack, msg = await handler.recv_msg('candidate_Test')
        print(ack, msg)
        p = await handler.send_msg('hello', 'candidate', 'Test', 2)
        print(p)
        c = await handler.ack(ack)
        print(c)
        time.sleep(1)
        print('周期完成')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())

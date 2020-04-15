from aiormq.types import DrainResult

from .pool import Pool


class ChannelSession(object):
    """
    提供和handler部分接口，入参返回完全一样
    使用此方法接收消息时，默认是手动ack模式
    """

    def __init__(self, pool: Pool):
        """非线程安全"""
        self.__pool = pool
        self.__channel = None

    async def __aenter__(self):
        self.__channel = await self.__pool._get()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.__channel is not None:
            self.__pool.put(self.__channel)

    # async def send_msg(self, msg: str, exchange: str, routing_key: str,
    #                    priority: int) -> typing.Optional[ConfirmationFrameType]:
    #     """
    #     发送消息 -> 默认持久化
    #     :param msg:
    #     :param exchange: 交换机名称
    #     :param routing_key: 路由关键字
    #     :param priority: 优先级 1-5 超过5将失效
    #     :return:
    #     """
    #     properties = spec.Basic.Properties(delivery_mode=2, priority=priority)
    #     return await self._do_query(
    #         func_name='basic_publish',
    #         exchange=exchange,
    #         routing_key=routing_key,
    #         body=msg.encode(),
    #         properties=properties)

    async def recv_msg(self, queue: str = '') -> tuple:
        msg = await self._do_query(func_name='basic_get', queue=queue, no_ack=False)
        if msg:
            method, properties, body, _ = msg
            if method is not None and isinstance(body, bytes):
                return method.delivery_tag, body.decode()
        return None, None

    async def _do_query(self, func_name, **kwargs):
        return await getattr(self.__channel, func_name)(**kwargs)

    # report ACK
    def ack(self, delivery_tag) -> DrainResult:
        return self._do_ack('basic_ack', delivery_tag)

    def nack(self, delivery_tag) -> DrainResult:
        return self._do_ack('basic_nack', delivery_tag)

    def _do_ack(self, func_name, delivery_tag):
        return getattr(self.__channel, func_name)(delivery_tag=delivery_tag)

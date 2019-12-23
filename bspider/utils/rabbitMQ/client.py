from functools import wraps

import pika

from bspider.config import FrameSettings
from bspider.utils import singleton


def retry(func):
    """重试失败的操作 最大三次"""
    @wraps(func)
    def _retry(self, *args, **kwargs):
        for i in range(3):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.close()
                self.__init__(self.mq_config)

    return _retry


@singleton
class RabbitMQClient(object):

    def __init__(self, mq_config):
        self.mq_config = mq_config
        if 'username' in mq_config and 'password' in mq_config:
            pika.ConnectionParameters()
            credentials = pika.PlainCredentials(mq_config['username'], mq_config['password'])
        else:
            credentials = None
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=mq_config['host'],
                port=mq_config['port'],
                credentials=credentials,
                virtual_host=mq_config.get('virtual_host', None),
            )
        )
        self.channel = self.connection.channel()
        self.queue_arg = FrameSettings()['QUEUE_ARG']

    def close(self):
        try:
            self.channel.close()
            self.connection.close()
        except Exception as e:
            return e

    # Exchange API

    @retry
    def exchange_declare(self, exchange: str):
        self.channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)

    # Queue API
    @retry
    def get_queue_message_count(self, queue):
        """
        获取队列的msg数量
        :param queue:
        :return:
        """
        result = self.declare_queue(queue)
        return result.method.message_count

    @retry
    def queue_declare(self, queue):
        """声明一个队列 新版pika"""
        return self.channel.queue_declare(
            queue=queue, durable=True, arguments=self.queue_arg)

    @retry
    def queue_delete(self, queue):
        """删除一个队列-- 这个方法会直接删除队列，很危险"""
        return self.channel.queue_delete(queue)

    @retry
    def queue_bind(self, queue, exchange, routing_key):
        """绑定一个队列"""
        self.channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

    @retry
    def send_msg(self, exchange, routing_key, body, priority=3):
        """默认使用消息持久化"""
        properties = pika.BasicProperties(delivery_mode=2, priority=priority)
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body, properties=properties)
        return True

    @retry
    def recv_msg(self, queue):
        """拉一条新的msg"""
        method, properties, body = self.channel.basic_get(queue=queue)
        # 队列是否为空
        if method is not None and isinstance(body, bytes):
            return method.delivery_tag, body.decode()
        return None, None

    @retry
    def report_acknowledgment(self, tag):
        """回ack给mq"""
        if isinstance(tag, int):
            self.channel.basic_ack(delivery_tag=tag)

    @retry
    def report_unacknowledgment(self, tag):
        if isinstance(tag, int):
            self.channel.basic_nack(delivery_tag=tag)

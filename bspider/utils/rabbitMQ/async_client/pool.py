"""
此处沿用
    https://github.com/mosquito/aio-pika/blob/master/aio_pika/pool.py 中的代码
    本项目中 采用 aiormq 作为底层库 而非 aio_pika
仅仅去掉 log句柄
"""
import asyncio
from typing import Callable, TypeVar, Any
from typing import AsyncContextManager, Coroutine


T = TypeVar("T")
ItemType = Coroutine[Any, None, T]
ConstructorType = Callable[..., ItemType]


class Pool(object):
    __slots__ = (
        'loop', '__max_size', '__items',
        '__constructor', '__created', '__lock',
        '__constructor_args'
    )

    def __init__(self, constructor: ConstructorType, *args, max_size: int =
                 None, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self.__max_size = max_size
        self.__items = asyncio.Queue(loop=self.loop)
        self.__constructor = constructor
        self.__constructor_args = args or ()
        self.__created = 0
        self.__lock = asyncio.Lock(loop=self.loop)

    def acquire(self) -> 'PoolItemContextManager':
        return PoolItemContextManager(self)

    @property
    def _has_released(self):
        return self.__items.qsize() > 0

    @property
    def _is_overflow(self) -> bool:
        if self.__max_size:
            return self.__created >= self.__max_size or self._has_released
        return self._has_released

    async def _create_item(self) -> T:
        async with self.__lock:
            if self._is_overflow:
                return await self.__items.get()

            # print('Creating a new instance of %r', self.__constructor)
            item = await self.__constructor(*self.__constructor_args)
            self.__created += 1
            return item

    async def _get(self) -> T:
        if self._is_overflow:
            channel = await self.__items.get()
            if channel.is_closed:
                # print('channel is close')
                self.__created -= 1
                channel = await self._create_item()
                # print('new a channel ', channel.is_closed)
            return channel

        return await self._create_item()

    def put(self, item: T):
        return self.__items.put_nowait(item)


class PoolItemContextManager(AsyncContextManager):
    __slots__ = 'pool', 'item'

    def __init__(self, pool: Pool):
        self.pool = pool
        self.item = None

    async def __aenter__(self) -> T:
        self.item = await self.pool._get()
        return self.item

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.item is not None:
            self.pool.put(self.item)

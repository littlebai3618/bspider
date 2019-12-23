from asyncio import iscoroutinefunction


class BaseCustomModule(object):

    async def _exec(self, func_name, *args):
        """用以支持协程和非协程编程方式"""
        func = getattr(self, func_name)
        if iscoroutinefunction(func):
            return await func(*args)
        else:
            return func(*args)
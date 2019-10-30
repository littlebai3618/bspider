# @Time    : 2019-07-31 18:40
# @Author  : 白尚林
# @File    : work
# @Use     :
import asyncio

from bspider.config import FrameSettings
from bspider.core import BaseManager
from .scheduler_monitor import SchedulerMonitor


def run_scheduler(coro_num=1):
    """A factory to make a download process"""
    coro_num = 1 if coro_num != 1 else coro_num
    dm = SchedulerManager(FrameSettings().get('SCHEDULER_SIGN', 'scheduler'), SchedulerMonitor)
    dm.run(coro_num)


class SchedulerManager(BaseManager):

    async def do_work(self):
        while True:
            for project_name, scheduler in self.monitor.projects.items():
                scheduler.scheduler()
            await asyncio.sleep(5)


if __name__ == '__main__':
    run_scheduler()

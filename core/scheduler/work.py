# @Time    : 2019-07-31 18:40
# @Author  : 白尚林
# @File    : work
# @Use     :
import asyncio

from core.scheduler.scheduler_monitor import SchedulerMonitor
from core.lib.base_manager import BaseManager


def run_scheduler(unique_sign, coro_num=50):
    """A factory to make a download process"""
    coro_num = 1 if coro_num != 1 else coro_num
    dm = SchedulerManager(unique_sign, SchedulerMonitor)
    dm.run(coro_num)


class SchedulerManager(BaseManager):

    async def do_work(self):
        while True:
            for project_name, scheduler in self.monitor.projects.items():
                scheduler.scheduler()
            await asyncio.sleep(5)


if __name__ == '__main__':
    run_scheduler('scheduler')

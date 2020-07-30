import asyncio

from bspider.config import FrameSettings
from bspider.core import BaseManager
from .scheduler_monitor import SchedulerMonitor


def run_scheduler(coro_num=1):
    """A factory to make a download process"""
    coro_num = 1 if coro_num != 1 else coro_num
    dm = SchedulerManager(FrameSettings().get('SCHEDULER_SIGN', 'default'), SchedulerMonitor, coro_num)
    dm.run()


class SchedulerManager(BaseManager):
    manager_type = 'scheduler'

    async def do_work(self):
        while True:
            self.log.debug('A new schedule start!')
            for project_id, scheduler in self.monitor.projects.items():
                await scheduler.scheduler(self.broker)
                self.log.debug(f'schedule project:project_id=>{project_id}!')
            self.log.info(f'A new schedule complete ! project_count=>{len(self.monitor.projects)}')
            await asyncio.sleep(1)


if __name__ == '__main__':
    run_scheduler()

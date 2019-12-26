import multiprocessing
import time

from bspider.agent import log
from bspider.core.api import BaseService, GetSuccess, PostSuccess, DeleteSuccess, Conflict, NotFound
from bspider.downloader.work import run_downloader
from bspider.parser.work import run_parser
from bspider.utils.system import System


class NodeService(BaseService):

    def __init__(self):
        """
        由于模块进程的特殊性，不能使用fork 方式产生多进程，必须采用spawn
        https://docs.python.org/3.6/library/multiprocessing.html?highlight=queue#multiprocessing.get_context
        """
        # 存储子worker对象
        self.module_list = {}
        self.mp_ctx = multiprocessing.get_context('spawn')

        self.system = System()

    def node_status(self):
        """报告 磁盘、处理器、内存使用状况"""
        return GetSuccess(
            msg='get node status success',
            data={
                'cpu_num': self.system.cpu_num,
                'cpu_percent': self.system.cpu_percent,
                'mem_size': self.system.mem_size,
                'mem_percent': self.system.mem_percent,
                'disk_size': self.system.disk_size,
                'disk_percent': self.system.disk_percent
            }
        )

    def start_worker(self, worker_id, worker_type, coroutine_num):
        unique_id = f'worker_{worker_id}'
        if unique_id in self.module_list:
            log.error(f'worker:worker_id->{worker_id} is already exist in this node')
            return Conflict(msg=f'worker:worker_id->{worker_id} is already exist in this node', errno=20001)

        if worker_type == 'downloader':
            func = run_downloader
        elif worker_type == 'parser':
            func = run_parser
        else:
            log.error(f'unknow worker type: {worker_type}')
            return Conflict(msg=f'unknow worker type: {worker_type}', errno=20002)

        worker = self.__start(func, unique_id, coroutine_num)
        if worker.is_alive():
            self.module_list[unique_id] = worker
            log.info(f'start work:{worker_id}-{worker_type} success')
            return PostSuccess(msg='worker process start success', data={'pid': worker.pid, 'status': 1})
        else:
            log.error(f'worker process start error. module start exec')
            return Conflict(msg=f'worker process start error', errno=20003)

    def __start(self, func, unique_id, coro_num):
        worker = self.mp_ctx.Process(name=unique_id, target=func, args=(unique_id, coro_num), daemon=True)
        worker.start()
        return worker

    def stop_worker(self, worker_id):
        unique_id = f'worker_{worker_id}'
        try:
            worker = self.module_list.pop(unique_id)
            log.info(f'delete worker:worker_id->{worker_id} success')
        except KeyError:
            log.warning(f'worker:worker_id->{worker_id} is not exist')
            return NotFound(msg=f'worker is not exist', errno=20004)

        try:
            while worker.is_alive():
                worker.terminate()
                time.sleep(0.5)
        except Exception as e:
            self.module_list[unique_id] = worker
            raise Conflict(f'worker stop error:{e}')
        return DeleteSuccess()

    def get_worker(self, worker_id):
        unique_id = f'worker_{worker_id}'
        worker = self.module_list.get(unique_id)
        if worker and worker.is_alive():
            return GetSuccess(data={'pid': worker.pid, 'status': 1})
        log.error(f'worker:worker_id->{worker_id} is not run')
        return GetSuccess(data={'pid': 0, 'status': -1})

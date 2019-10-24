# @Time    : 2019/7/17 2:23 PM
# @Author  : 白尚林
# @File    : node
# @Use     :
"""采集node 信息"""
import multiprocessing
import time

from bspider.agent import log
from bspider.core.api import BaseService, GetSuccess, PostSuccess, DeleteSuccess, Conflict, NotFound
from bspider.core.downloader.work import run_downloader
from bspider.core.parser.work import run_parser
from bspider.utils.system import cpu_used, mem_used, disk_used, process_info


class NodeService(BaseService):

    def __init__(self):
        """
        由于模块进程的特殊性，不能使用fork 方式产生多进程，必须采用spawn
        https://docs.python.org/3.6/library/multiprocessing.html?highlight=queue#multiprocessing.get_context
        """
        # 存储子worker对象
        self.module_list = {}
        self.mp_ctx = multiprocessing.get_context('spawn')

    def node_status(self):
        """报告 磁盘、处理器、内存使用状况"""
        return GetSuccess(
            msg='get node status success',
            data={
                'cpu': cpu_used(),
                'memory': mem_used(),
                'disk': disk_used()
            }
        )

    def start_worker(self, name, worker_type, coro_num):
        if name in self.module_list:
            log.error(f'worker {name} is already exist in this node')
            return Conflict(msg=f'worker {name} is already exist in this node', errno=20001)

        if worker_type == 'downloader':
            func = run_downloader
        elif worker_type == 'parser':
            func = run_parser
        else:
            log.error(f'unknow worker type: {worker_type}')
            return Conflict(msg=f'unknow worker type: {worker_type}', errno=20002)

        worker = self.__start(func, name, coro_num)
        if worker.is_alive():
            self.module_list[name] = worker
            log.info(f'start work:{name}-{worker_type} success')
            return PostSuccess(msg='worker process start success',
                               data={'pid': worker.pid, 'name': worker.name, 'type': worker_type})
        else:
            log.error(f'worker process start error. module start exec')
            return Conflict(msg=f'worker process start error', errno=20003)

    def __start(self, func, name, coro_num):
        worker = self.mp_ctx.Process(name=name, target=func, args=(name, coro_num), daemon=True)
        worker.start()
        return worker

    def stop_worker(self, name):
        try:
            worker = self.module_list.pop(name)
        except KeyError:
            log.error(f'worker:{name} is not exist')
            return NotFound(msg=f'worker:{name} is not exist', errno=20004)
        while worker.is_alive():
            worker.terminate()
            time.sleep(0.5)
        log.info(f'delete worker:{name} success')
        return DeleteSuccess()

    def get_worker(self, name):
        worker = self.module_list.get(name)
        if worker:
            tmp = self.__get_process_info(worker)
            return GetSuccess(data=tmp)
        log.error(f'worker:{name} is not exist')
        return NotFound(msg=f'worker:{name} is not exist', errno=20004)

    def get_workers(self):
        result = []
        for name, worker in self.module_list.items():
            tmp = self.__get_process_info(worker)
            result.append(tmp)
        return GetSuccess(data=result)

    @staticmethod
    def __get_process_info(worker):
        result = process_info(worker.pid)
        result['pid'] = worker.pid
        result['unique_key'] = worker.name
        result['status'] = 1 if worker.is_alive else 0
        return result

    def worker_status(self):
        """返回所有子进程的运行状态"""
        result = {}
        for name, worker in self.module_list.items():
            result[name] = worker.is_alive
        return GetSuccess(data=result)

    def __del__(self):
        for name, worker in self.module_list.items():
            while worker.is_alive():
                worker.terminate()

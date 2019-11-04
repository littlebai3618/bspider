# @Time    : 2018/10/11 下午4:25
# @Author  : 白尚林
# @File    : system
# @Use     : 获取系统相关信息
"""
这里实例化一个对象，启用单独的线程异步获取CPU\DESK\MEM 使用率、系统配置
"""

import psutil

from bspider.config import FrameSettings


class System(object):
    """
    #### 后续增加异步获取CPU等使用率
    """
    ip_msg = '{}->{}'.format(FrameSettings()['MASTER']['ip'], FrameSettings()['AGENT']['ip'])

    @property
    def cpu_percent(self):
        return psutil.cpu_percent()

    @property
    def mem_percent(self):
        return psutil.virtual_memory().percent

    @property
    def disk_percent(self):
        return psutil.disk_usage('/').percent

    @property
    def cpu_num(self):
        return psutil.cpu_count(logical=True)

    @property
    def mem_size(self):
        """返回字节大小"""
        return psutil.virtual_memory().total

    @property
    def disk_size(self):
        return psutil.disk_usage('/').total


class WorkerProcess():
    pass


if __name__ == '__main__':
    print(System().cpu_percent)

    ps_info = {
        'CPU COUNT': psutil.cpu_count(),
        'CPU PERCENT': psutil.cpu_percent(),
        'MEM SIZE': psutil.virtual_memory().total,
        'MEM PERCENT': psutil.virtual_memory().percent,
        'DISK SIZE': psutil.disk_usage('/').total,
        'DISK PERCENT': psutil.disk_usage('/').percent
    }

    for key, value in ps_info.items():
        print(f'{key}:{value}')

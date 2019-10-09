# @Time    : 2018/10/11 下午4:25
# @Author  : 白尚林
# @File    : system
# @Use     : 获取系统相关信息
import psutil

from bspider.config import FrameSettings


def cpu_used():
    """获取CPU使用率"""
    return psutil.cpu_percent(interval=0.1)


def mem_used():
    """获取内存使用率"""
    memory = psutil.virtual_memory()
    return memory.percent


def disk_used():
    """获取磁盘使用率"""
    disk = psutil.disk_usage('/')
    return disk.percent

__ip_addr = '{}->{}'.format(FrameSettings()['MASTER']['ip'], FrameSettings()['AGENT']['ip'])
def ip_addr():
    """获取机器内网ip"""
    return __ip_addr
def process_info(pid):
    p = psutil.Process(pid)
    status = p.is_running()
    try:
        mem = p.memory_percent()
        return {'mem': mem, 'status': status}
    except Exception as e:
        return {'mem': None, 'err': f"{e}", 'status': status}


if __name__ == '__main__':
    print(ip_addr())

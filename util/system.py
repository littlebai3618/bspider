# @Time    : 2018/10/11 下午4:25
# @Author  : 白尚林
# @File    : system
# @Use     : 获取系统相关信息
import psutil

from config import node_settings


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

def ip_addr():
    """获取机器内网ip"""
    try:
        return node_settings.IP
    except AttributeError:
        ip_list = psutil.net_if_addrs()
        if 'eth0' in ip_list:
            ip = ip_list['eth0'][0].address
        else:
            ip = ip_list['eth1'][0].address
        return ip


def process_info(pid):
    p = psutil.Process(pid)
    status = p.is_running()
    try:
        mem = p.memory_percent()
        return {'mem': mem, 'status': status}
    except Exception as e:
        return {'mem': None, 'err': f"{e}", 'status': status}


if __name__ == '__main__':
    print(cpu_used())

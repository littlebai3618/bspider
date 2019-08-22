# @Time    : 2019/7/11 3:41 PM
# @Author  : 白尚林
# @File    : formatter
# @Use     :
import json
import logging

from util.system import ip_addr


def get_json_formatter(**kwargs):
    """返回指定的log formatter"""
    log_from_work = {
        'time': '%(asctime)s',
        'pid': '%(process)d',
        'filename': '%(filename)s:%(lineno)d',
        'level': '%(levelname)s',
        'node': ip_addr(),
        'msg': '%(message)s',
    }
    for key,value in kwargs.items():
        if key in log_from_work:
            continue
        log_from_work[key] = value
    return logging.Formatter(json.dumps(log_from_work))

def get_stream_formatter(**kwargs):
    log_from_work = '[%(asctime)s] [%(filename)s:%(lineno)d] [node:{}] {} [%(levelname)s] [%(message)s]'
    arg = ' '.join([f'[{key}:{value}]' for key,value in kwargs.items()])
    return logging.Formatter(log_from_work.format(ip_addr(), arg))
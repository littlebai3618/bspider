import json
import logging

from bspider.utils.system import System


def get_json_formatter(**kwargs):
    """返回指定的log formatter"""
    log_from_work = {
        'time': '%(asctime)s',
        'pid': '%(process)d',
        'filename': '%(filename)s:%(lineno)d',
        'level': '%(levelname)s',
        'node': System.ip_msg,
        'msg': '%(message)s',
    }
    for key, value in kwargs.items():
        if key in log_from_work:
            continue
        log_from_work[key] = value
    return logging.Formatter(json.dumps(log_from_work))


def get_stream_formatter(**kwargs):
    arg = ' '.join([f'{value}' for key, value in kwargs.items() if key == 'module'])
    log_from_work = f'[%(asctime)s {arg} %(process)d %(filename)s:%(lineno)s] %(levelname)s: %(message)s'
    return logging.Formatter(log_from_work)

def get_file_formatter(**kwargs):
    arg = ' '.join([f'{key}={value}' for key, value in kwargs.items()])
    log_from_work = f'[%(asctime)s %(process)d %(filename)s:%(lineno)s] %(levelname)s: ({arg}) %(message)s'
    return logging.Formatter(log_from_work)

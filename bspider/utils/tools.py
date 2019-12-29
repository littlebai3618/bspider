"""
常用工具封装
"""
import asyncio
import hashlib
import re
import time


def make_sign(url, salt=''):
    return '{}-{}'.format(hashlib.md5(f'{url}{salt}'.encode('utf-8')).hexdigest(), time.time())


def coroutine_result(coroutine, loop=None):
    """a function to get coroutine return"""
    if loop is None:
        loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(coroutine, loop=loop)
    loop.run_until_complete(task)
    return task.result()


def change_dict_key(cur_key, replace_key, d: dict) -> dict:
    if cur_key in d:
        d[replace_key] = d.pop(cur_key)
    return d


def make_fields_values(data: dict) -> tuple:
    """
    给定字典，返回fields 和 values
    :param info: dict
    :return:
    """
    fields = ','.join([' `%s`=%%s ' % (key) for key in data.keys()])
    values = [data[key] for key in data.keys()]
    return fields, tuple(values)


def find_class_name_by_content(content):
    reg = re.compile('class (?P<class_name>.*?)\((?P<sub_class_name>.*?)\):').search(content)
    if reg:
        tmp = reg.groupdict()
        return True, tmp['class_name'], tmp['sub_class_name']
    return False, None, None

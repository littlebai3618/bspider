"""
常用工具封装
"""
import asyncio
import datetime
import hashlib
import json
import re
import time

from apscheduler.triggers.cron import CronTrigger
from apscheduler.util import datetime_to_utc_timestamp

from bspider.utils.exceptions import ModuleError


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
    fields = list()
    values = list()
    for key, value in data.items():
        fields.append(' `%s`=%%s ' % (key))
        if isinstance(value, dict) or isinstance(value, list):
            values.append(json.dumps(value))
        else:
            values.append(value)

    return ','.join(fields), tuple(values)


def find_class_name_by_content(content):
    reg = re.compile('class (?P<class_name>.*?)\((?P<sub_class_name>.*?)\):').search(content)
    if reg:
        tmp = reg.groupdict()
        return tmp['class_name'], tmp['sub_class_name']
    raise ModuleError('content can\'t find class_name and sub_class_name -> \n%s' % (content[0: 100] + ' ...'))


def module_name2class_name(module_name):
    """
    python 的模块名改为类名
    demo_pipeline -> DemoPipeline
    """
    return ''.join([word.title() for word in module_name.lower().split('_')])

def class_name2module_name(class_name):
    """
    python 的模块名改为类名
    DemoPipeline -> demo_pipeline
    """
    pattern = re.compile(r'([A-Z]{1})')
    return re.sub(pattern, r'_\1', class_name).lower().replace('_', '', 1)

def get_crontab_next_run_time(crontab, tz = None):
    crontab = CronTrigger.from_crontab(crontab)
    now = datetime.datetime.now(tz)
    next_run_time = crontab.get_next_fire_time(None, now)
    return datetime_to_utc_timestamp(next_run_time), next_run_time


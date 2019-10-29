# @Time    : 2019/6/16 1:43 PM
# @Author  : 白尚林
# @File    : tools
# @Use     :
"""
常用工具封装
"""
import asyncio
import hashlib
import re
import time


def hump2underline(hunp_str):
    '''
    驼峰形式字符串转成下划线形式
    :param hunp_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub

def underline2hump(underline_str):
    '''
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    '''
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)',lambda x:x.group(1)[1].upper(),underline_str)
    return sub

def is_ip(ip_str):
    pattern = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
    return True if len(pattern.findall(ip_str)) else False

def make_sign(project_name, url, salt=''):
    plaintext = '{}{}'.format(url, salt).encode('utf-8')
    return '{}:{}:{}'.format(project_name, hashlib.md5(plaintext).hexdigest(), time.time())

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

def find_class_name_by_content(content):
    reg = re.compile('class (?P<class_name>.*?)\((?P<sub_class_name>.*?)\):').search(content)
    if reg:
        tmp = reg.groupdict()
        return True, tmp['class_name'], tmp['sub_class_name']
    return False, None, None


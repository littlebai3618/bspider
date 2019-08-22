# @Time    : 2019/7/17 12:59 PM
# @Author  : 白尚林
# @File    : __init__.py
# @Use     :
from util.logger import LoggerPool

log = LoggerPool().get_logger('agent', module='agent')

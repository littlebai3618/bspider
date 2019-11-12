# @Time    : 2019/7/17 12:59 PM
# @Author  : 白尚林
# @File    : __init__.py
# @Use     :
from bspider.utils.logger import LoggerPool
from bspider.utils.system import System

log = LoggerPool().get_logger(key='agent', fn='agent', module=f'agent', ip=System.ip_msg)
# 注册一个Auth模块的句柄
LoggerPool().get_logger(key='api_auth', fn='agent', module='api_auth')

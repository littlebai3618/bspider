# @Time    : 2019/6/18 12:55 PM
# @Author  : 白尚林
# @File    : __init__.py
# @Use     :
from bspider.utils.logger import LoggerPool
from bspider.utils.system import System

log = LoggerPool().get_logger(key='master', fn='master', module=f'master', ip=System.ip_msg)

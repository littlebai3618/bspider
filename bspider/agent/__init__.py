from bspider.utils.logger import LoggerPool
from bspider.utils.system import System

log = LoggerPool().get_logger(key='agent', fn='agent', module=f'agent', ip=System.ip_msg)
# 注册一个Auth模块的句柄，用来实现复用模块日志输出至不同文件的功能
LoggerPool().get_logger(key='api_auth', fn='agent', module='api_auth')

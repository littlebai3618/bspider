from bspider.utils.logger import LoggerPool
from bspider.utils.system import System

log = LoggerPool().get_logger(key='agent', fn='agent', module=f'agent', ip=System.ip_msg)

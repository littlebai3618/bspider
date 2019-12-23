from bspider.utils.logger import LoggerPool

log = LoggerPool().get_logger(key='master', fn='master', module=f'master')
# 注册一个Auth模块的句柄
LoggerPool().get_logger(key='api_auth', fn='master', module='api_auth')


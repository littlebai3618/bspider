# 全局程序运行模式 development | produce
GLOBAL_PATTERN = 'development'
# 节点内网IP 非必须配置，如配置则按照配置
MASTER_SERVICE = 'http://127.0.0.1:5000'
AGENT_SERVICE = 'http://127.0.0.1:5001'

WEB_STUDIO_DB = {
    'MYSQL_HOST': '',
    'MYSQL_PORT': 3306,
    'MYSQL_USER': '',
    'MYSQL_PASSWD': '',
    'MYSQL_CHARSET': 'utf8',
    'MYSQL_DB': '',
}

TZ = 'Asia/Shanghai'  # utc +8

WEB_SECRET_KEY = ''
# token 认证有效时间 s 这里设置为5日
WEB_TOKEN_LIVE_TIME = 3600 * 5

# rabbitmq
RABBITMQ_CONFIG = {
    'host': '',
    'port': 5672,
    'username': '',
    'password': '',
    'virtual_host': '',
}

#################
# 节点监控相关配置 #
#################
SUPERVISOR_RPC = ('', '', 9010)

#################
# 定时任务相关配置 #
#################
# 定时任务启动线程数量
CRON_JOB_THREAD_NUM = 20
# 定时任务启动进程数量
CRON_JOB_PROCESS_NUM = 1
# 定时任务刷新时间 s
CRON_JOB_REFRESH_TIME = 3

#################
# 代码加载模块配置 #
#################


#################
# 消息通知模块配置 #
#################
# 重要配置不可为空
DING = ''

#################
# 下载器配置 #
#################

#################
# 日志模块配置 #
#################
LOGGER_EXCHANGE_NAME = 'logger'
LOGGER_QUEUE_NAME = 'bspider_logger'
LOGGER_LEVEL = 'DEBUG'

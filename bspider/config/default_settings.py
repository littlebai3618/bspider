GLOBAL_PATTERN = 'development'

TIMEZONE = 'Asia/Shanghai'
WEB_TOKEN_LIVE_TIME = 3600 * 5

#################
# 节点监控相关配置 #
#################

#################
# 定时任务相关配置 #
#################
CRON_JOB_THREAD_NUM = 20
CRON_JOB_PROCESS_NUM = 1
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

# *** 内置配置
# 存储抓取任务的表
PROJECT_TABLE = 'bspider_project'
# 存储用户信息的表
USER_TABLE = 'bspider_user'
# 存储鉴权信息的表
AUTH_RULE_TABLE = 'bspider_casbin_auth'
# 节点列表
NODE_TABLE = 'bspider_node'
# worker列表
WORKER_TABLE = 'bspider_worker'
# 节点状态列表
NODE_STATUS_TABLE = 'bspider_node_status'
# 定时任务调度表
CRON_JOB_STORE_TABLE = 'bspider_cronjob'
# 远程代码仓库表
CODE_STORE_TABLE = 'bspider_customcode'
# 关联表
P2C_TABLE = 'bspider_project_customcode'
# 任务下载状态存储表
DOWNLOADER_STATUS_TABLE = 'bspider_downloader_status'
# 任务解析状态存储表
PARSER_STATUS_TABLE = 'bspider_parser_status'
# rabbitmq - exchange 表
EXCHANGE_NAME = ('candidate', 'download', 'parse')
# order key
OREDR_KEY = 'order'
# queue arg
QUEUE_ARG = {"x-max-priority": 5, "x-queue-mode": 'lazy'}

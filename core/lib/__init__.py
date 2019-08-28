# @Time    : 2019/7/2 2:31 PM
# @Author  : 白尚林
# @File    : __init__.py
# @Use     :
import pytz

from config import frame_settings

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
#
TZ = pytz.timezone(frame_settings.TZ)
# queue arg
QUEUE_ARG = {"x-max-priority": 10, "x-queue-mode": 'lazy'}

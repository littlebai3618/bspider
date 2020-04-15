# 运行模式，本地开发请使用development，服务部署请使用produce
# development log 输出至终端
# produce log 输出至文件
GLOBAL_PATTERN = 'development'
LOGGER_LEVEL = 'DEBUG'

#################
# MASTER模块配置 #
#################
# 各节点的 AGENT 进程将会通过访问 http://ip:port 和主进程进行通信
# web studio访问地址：http://ip:port
# ****************************************************
# web studio 默认用户: 账号admin，密码admin 请登录后尽快修改
# ****************************************************

# 时区配置 str
TIMEZONE = 'Asia/Shanghai'

# JWT Token 生效时间
WEB_TOKEN_LIVE_TIME = 3600 * 5

# 定时任务进程启动多少工作线程用以执行定时任务
CRON_JOB_THREAD_NUM = 20
# 多久同步一次定时任务信息，单位s, 数字越小效果越好，数字越大性能消耗越小
CRON_JOB_REFRESH_TIME = 3

#################
# AGENT  模块配置 #
#################
# master节点将通过访问 http://ip:port 和 当前节点agent进行通信

#################
# RABBITMQ 配置  #
#################

#################
# supervisor配置 #
#################
SUPERVISOR_RPC_PORT = 9010
SUPERVISOR_RPC = {
    'username': 'bspider_node',
    'password': 'bspider_node',
    'port': SUPERVISOR_RPC_PORT
}

#################
# 消息通知模块配置 #
#################

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
CRON_JOB_STORE_TABLE = 'bspider_cron'
# 远程代码仓库表
CODE_STORE_TABLE = 'bspider_customcode'
# 关联表
P2C_TABLE = 'bspider_project_customcode'
# 任务下载状态存储表
DOWNLOADER_STATUS_TABLE = 'bspider_downloader_status'
# 任务解析状态存储表
PARSER_STATUS_TABLE = 'bspider_parser_status'
# rabbitmq - exchange
EXCHANGE_NAME = ('candidate', 'download', 'parse')
# order key
OREDR_KEY = 'order'
# queue arg
QUEUE_ARG = {"x-max-priority": 5, "x-queue-mode": 'lazy'}

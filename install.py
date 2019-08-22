# @Time    : 2019-08-22 16:08
# @Author  : 白尚林
# @File    : install
# @Use     :
"""
1. 初始化supervisor 配置文件
2. 初始化gunicorn 配置文件
"""
import os

from config import frame_settings

supervisor = """[unix_http_server]                                                                                                                                                                             
file={root_path}/cache/supervisor.sock;
[supervisord]
logfile={root_path}/log/supervisord.log;
loglevel={loglevel};
pidfile={root_path}/cache/supervisord.pid;
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
[supervisorctl]
serverurl=unix://{root_path}/cache/supervisor.sock ;

[inet_http_server]
port=0.0.0.0:{supervisor_port}
username={supervisor_username}
password={supervisor_password}

[program:agent]
command=gunicorn -c {root_path}/cache/gunicorn.py --chdir {root_path}/ agent_manager:app;
directory={root_path}
user=bspider
startsecs=0;
stopwaitsecs=0;
autostart=false;
autorestart=true;
stdout_logfile={root_path}/log/agent.log;
stderr_logfile={root_path}/log/agent.log;


"""

gunicorn = """import gevent.monkey
gevent.monkey.patch_all()
loglevel = {loglevel}
bind = '{agent_service}'
pidfile = '{root_path}/cache/gunicorn.pid'
workers = 1
worker_connections = 2000
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'"""

bash = """#!/bin/sh

process_type="$1"

export PYTHONPATH=%s:${PYTHONPATH}

if [ "$process_type" != "agent" ] && [ "$process_type" == "master" ] ; then
    echo "unknow process_type ${process_type}"
    exit 255
else
    echo "try to start ${process_type}"
    nohup supervisor -c %s/supervisor.conf >%s/supervisor.log 2>&1 &
    echo "please check ${process_type} process:"
    echo "tail -f log/supervisor.log"
fi"""

root_path = os.path.abspath('.')
init_dict = dict(
    root_path=root_path,
    loglevel=frame_settings.LOGGER_LEVEL,
    agent_service=frame_settings.AGENT_SERVICE,
    supervisor_username=frame_settings.SUPERVISOR_RPC[0],
    supervisor_password=frame_settings.SUPERVISOR_RPC[1],
    supervisor_port=frame_settings.SUPERVISOR_RPC[2],
)

with open(f'{root_path}/cache/supervisor.conf', 'w') as f:
    f.write(supervisor.format(**init_dict))

with open(f'{root_path}/cache/gunicorn.py', 'w') as f:
    f.write(gunicorn.format(**init_dict))

with open(f'{root_path}/start.sh', 'w') as f:
    f.write(bash % (root_path, root_path, root_path))
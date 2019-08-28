# @Time    : 2019-08-22 16:08
# @Author  : 白尚林
# @File    : install
# @Use     :
"""
1. 初始化supervisor 配置文件
2. 初始化gunicorn 配置文件
"""
import os
import sys

from bin.gunicorn import make_gunicorn_conf
from bin.supervisor import make_supervisor_conf
from config import frame_settings


bash = """#!/bin/sh
export PYTHONPATH={root_path}:$|PYTHONPATH|

echo "try to start by model: {process_type}"
nohup supervisord -c {root_path}/supervisor_{process_type}.conf >{root_path}/supervisor_{process_type}.log 2>&1 &
echo "please check {process_type} process:"
echo "tail -f log/supervisor_{process_type}.log"
    
fi"""

if __name__ == '__main__':
    root_path = os.path.abspath('.')
    init_dict = dict(
        root_path=root_path,
        loglevel=frame_settings.LOGGER_LEVEL.lower(),
        agent_service=frame_settings.AGENT_SERVICE.replace('http://', '').replace('https://', ''),
        master_service=frame_settings.MASTER_SERVICE.replace('http://', '').replace('https://', ''),
        supervisor_username=frame_settings.SUPERVISOR_RPC[0],
        supervisor_password=frame_settings.SUPERVISOR_RPC[1],
        supervisor_port=frame_settings.SUPERVISOR_RPC[2],
    )
    process_type = sys.argv[1]
    make_supervisor_conf(root_path, process_type, **init_dict)
    make_gunicorn_conf(root_path, **init_dict)

    with open(f'{root_path}/start.sh', 'w') as f:
        f.write(bash.format(root_path=root_path, process_type=process_type).replace('$|PYTHONPATH|', '${PYTHONPATH}'))
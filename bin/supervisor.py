# @Time    : 2019-08-27 14:04
# @Author  : 白尚林
# @File    : supervisor
# @Use     :


def make_supervisor_conf(path, install_type='single_node', **kwargs):
    base = """[unix_http_server]                                                                                                                                                                             
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

    """

    agent = """[program:agent]
    command=gunicorn -c {root_path}/cache/gunicorn.py --chdir {root_path}/ agent_manager:app;
    directory={root_path}
    user=bspider
    startsecs=0;
    stopwaitsecs=0;
    autostart=false;
    autorestart=true;
    stdout_logfile={root_path}/log/agent.log;
    stderr_logfile={root_path}/log/agent.log;"""

    master = """[program:master]
    command=gunicorn -c {root_path}/cache/gunicorn.py --chdir {root_path}/ master_manager:app;
    directory={root_path}
    user=bspider
    startsecs=0;
    stopwaitsecs=0;
    autostart=true;
    autorestart=true;
    stdout_logfile={root_path}/log/master.log;
    stderr_logfile={root_path}/log/master.log;"""
    if install_type == 'single_node':
        with open(f'{path}/cache/supervisor_single_node.conf', 'w') as f:
            f.write(f'{base}\n{agent}\n{master}'.format(**kwargs))
    else:
        with open(f'{path}/cache/supervisor_agent.conf', 'w') as f:
            f.write(f'{base}\n{agent}'.format(**kwargs))

        with open(f'{path}/cache/supervisor_master.conf', 'w') as f:
            f.write(f'{base}\n{master}'.format(**kwargs))

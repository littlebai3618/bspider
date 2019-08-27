# @Time    : 2019-08-27 14:24
# @Author  : 白尚林
# @File    : gunicorn
# @Use     :


def make_gunicorn_conf(path, **kwargs):
    agent = """import gevent.monkey
gevent.monkey.patch_all()
loglevel = '{loglevel}'
bind = '{agent_service}'
pidfile = '{root_path}/cache/agent_gunicorn.pid'
workers = 1
worker_connections = 2000
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'"""

    master = """import gevent.monkey
gevent.monkey.patch_all()
loglevel = '{loglevel}'
bind = '{master_service}'
pidfile = '{root_path}/cache/master_gunicorn.pid'
workers = 1
worker_connections = 2000
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'"""
    with open(f'{path}/cache/master_gunicorn.py', 'w') as f:
        f.write(master.format(**kwargs))
    with open(f'{path}/cache/agent_gunicorn.py', 'w') as f:
        f.write(agent.format(**kwargs))

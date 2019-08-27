# @Time    : 2019-08-27 14:24
# @Author  : 白尚林
# @File    : gunicorn
# @Use     :


def make_gunicorn_conf(path, **kwargs):
    gunicorn = """import gevent.monkey
gevent.monkey.patch_all()
loglevel = {loglevel}
bind = '{agent_service}'
pidfile = '{root_path}/cache/gunicorn.pid'
workers = 1
worker_connections = 2000
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'"""
    with open(f'{path}/cache/supervisor.conf', 'w') as f:
        f.write(gunicorn.format(**kwargs))

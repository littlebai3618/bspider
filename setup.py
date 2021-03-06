from setuptools import setup, find_packages

extras_require = {}

setup(
    name='bspider',
    version=open('./bspider/VERSION').read().strip(),
    description='A high-level distributed crawling framework Git: https://github.com/littlebai3618/bspider',
    author='baii',
    author_email='2624386844@qq.com',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['bspider = bspider.cmdline:execute']
    },
    classifiers=[
        'Framework :: Scrapy',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=[
        'aiohttp==3.6.2',
        'aiomysql==0.0.20',
        'aiormq==2.7.2',
        'APScheduler==3.6.1',
        'asn1crypto==0.24.0',
        'async-timeout==3.0.1',
        'attrs==19.1.0',
        'casbin==0.7.1',
        'certifi==2019.6.16',
        'cffi==1.12.3',
        'chardet==3.0.4',
        'Click==7.0',
        'cryptography==2.7',
        'DBUtils==1.3',
        'Flask==1.1.1',
        'Flask-Cors==3.0.8',
        'Flask-HTTPAuth==3.3.0',
        'Flask-WTF==0.14.2',
        'gevent==1.4.0',
        'greenlet==0.4.15',
        'gunicorn==19.9.0',
        'idna==2.8',
        'itsdangerous==1.1.0',
        'Jinja2==2.10.1',
        'lxml==4.4.1',
        'MarkupSafe==1.1.1',
        'meld3==1.0.2',
        'multidict==4.5.2',
        'pamqp==2.3.0',
        'pika==1.1.0',
        'psutil>=5.6.6',
        'pycparser==2.19',
        'PyMySQL==0.9.2',
        'pytz==2019.2',
        'requests==2.22.0',
        'simpleeval==0.9.8',
        'six==1.12.0',
        'supervisor==4.0.4',
        'tzlocal==2.0.0',
        'urllib3==1.25.3',
        'Werkzeug==0.15.5',
        'WTForms==2.2.1',
        'xpinyin==0.5.6',
        'yarl==1.3.0',
        'redis==3.3.11',
        'PyYAML==5.2',
        'voluptuous==0.11.7'
    ],
    extras_require=extras_require,
)

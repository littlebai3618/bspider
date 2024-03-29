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
        "aiohttp==3.7.4.post0",
        "aiomysql==0.0.21",
        "aiormq==2.7.2",
        "APScheduler==3.7.0",
        "DBUtils==1.3",
        "Flask==2.0.0",
        "Flask-Cors==3.0.10",
        "Flask-HTTPAuth==4.3.0",
        "Flask-WTF==0.14.3",
        "gevent==21.1.2",
        "gunicorn==20.1.0",
        "pika==1.2.0",
        "psutil==5.8.0",
        "pytz==2021.1",
        "PyYAML==5.4.1",
        "redis==3.5.3",
        "requests==2.25.1",
        "supervisor==4.2.2",
        "WTForms==2.3.3",
        "xpinyin==0.7.6",
    ],
    extras_require=extras_require,
)

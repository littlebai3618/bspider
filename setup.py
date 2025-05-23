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
        "aiohttp==3.11.18",
        "aiomysql==0.2.0",
        "aiormq==6.8.0",
        "APScheduler==3.10.4",
        "DBUtils==3.0.3",
        "Flask==3.1.1",
        "Flask-Cors==4.0.0",
        "Flask-HTTPAuth==4.8.0",
        "Flask-WTF==1.2.1",
        "gevent==24.2.1",
        "gunicorn==22.0.0",
        "pika==1.3.2",
        "psutil==5.9.8",
        "pytz==2024.1",
        "PyYAML==6.0.2",
        "redis==6.1.0",
        "requests==2.32.3",
        "supervisor==4.2.5",
        "WTForms==3.1.2",
        "xpinyin==0.7.6",
    ],
    extras_require=extras_require,
)

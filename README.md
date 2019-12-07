======
Scrapy
======

.. image:: https://img.shields.io/pypi/v/Scrapy.svg
   :target: https://pypi.python.org/pypi/Scrapy
   :alt: PyPI Version

.. image:: https://img.shields.io/badge/python-%3E=3.7-brightgreen.svg
   :target: https://pypi.python.org/pypi/Scrapy
   :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/wheel-yes-brightgreen.svg
   :target: https://pypi.python.org/pypi/Scrapy
   :alt: Wheel Status


简介
========

BSpider 是一个纯Python实现的高等级分布式全异步web抓取框架，框架采用多进程 + 
协程的方式规避 GIL锁带来的不良影响，充分利用多核CPU性能，同时框架设计上尽可能的
减少框架自身对系统性能的影响，使尽可能多的计算资源用于抓取、解析操作。

前置依赖
============

* Python 3.7+
* 框架服务职能部署在 Linux, Mac OSX 系统
* 可以在 Linux, Windows, Mac OSX 系统进行爬虫开发
* rabbtmq 3.7+ 并启用 rabbitmq management plugins 提供可访问插件的账号
* MySQL 5.x+

安装
=======

快速安装:

    pip install bspider

或从此git仓库自行安装

快速开始
=============
启动服务
1. bspider startplatform ${platform_name} # 初始化工作台
2. vim ${platform_name}/config/frame_settings.py # 填入配置
3. bspider master start # 启动master节点 
========

You can check https://docs.scrapy.org/en/latest/news.html for the release notes.

Community (blog, twitter, mail list, IRC)
=========================================

See https://scrapy.org/community/ for details.

Contributing
============

See https://docs.scrapy.org/en/master/contributing.html for details.

Code of Conduct
---------------

Please note that this project is released with a Contributor Code of Conduct
(see https://github.com/scrapy/scrapy/blob/master/CODE_OF_CONDUCT.md).

By participating in this project you agree to abide by its terms.
Please report unacceptable behavior to opensource@scrapinghub.com.

Companies using Scrapy
======================

See https://scrapy.org/companies/ for a list.

Commercial Support
==================

See https://scrapy.org/support/ for details.

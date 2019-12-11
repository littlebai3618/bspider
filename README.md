<p align="center">
  <h1>BSpider</h1>
</p>
<p align="center">
  <a href="https://github.com/python">
    <img src="https://img.shields.io/badge/Python-3.7.4-brightgreen.svg" alt="Python">
  </a>
  <a href="https://github.com/PanJiaChen/vue-admin-template">
    <img src="https://img.shields.io/badge/vue--admin--template-4.0+-brightgreen.svg" alt="vue-admin-template">
  </a>
</p>

简介
========

BSpider 是一个纯Python实现的高等级分布式全异步web抓取框架，框架采用多进程 + 
协程的方式规避 GIL锁带来的不良影响，充分利用多核CPU性能，同时框架设计上尽可能的
减少框架自身对系统性能的影响，使尽可能多的计算资源用于抓取、解析操作。

前置依赖
============

* Python 3.7+
* 框架服务只能部署在 Linux, Mac OSX 系统
* 可以在 Linux, Windows, Mac OSX 系统进行开发
* rabbtmq >3.7.x 并启用 rabbitmq management plugins 提供可访问插件的账号
* MySQL >5.x

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
3. bspider master start # 启动master节点第一次启动节点会初始化MySQL表
4. bspider agent start # 根据配置启动工作节点

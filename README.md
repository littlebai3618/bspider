<p align="center">
    BSpider
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
* rabbtmq `>3.7.x` 并启用 `rabbitmq management plugins` 提供可访问插件的账号
* MySQL `>5.x`

安装
=======

快速安装:

    pip install bspider

或从此git仓库自行安装

## 快速开始
=============
### 多节点
启动master
```shell script
bspider startplatform ${platform_name} # 初始化工作台
vim ${platform_name}/config/frame_settings.py # 填入配置
bspider master start # 启动master节点第一次启动节点会初始化MySQL表
```
> notice:
> 1. bspider-studio默认账号：admin 密码：admin
> 2. 登录地址 http://${frame_settings.MASTER.ip}:{frame_settings.MASTER.port} `此处建议使用默认配置并配置nginx进行端口转发`

启动agent
```shell script
bspider startplatform ${platform_name} # 初始化工作台
vim ${platform_name}/config/frame_settings.py # 填入配置
bspider agent start # 、初次启动agent需要使用命令行进行启动，后续可在bspider-studio进行管理
```
> notice:
> 1. agent frame_settings 除agent 配置以外其他配置应和master 保持一致 `AGENT.ip需 和 MASTER.ip 互访`

### 单节点
```shell script
bspider startplatform ${platform_name} # 初始化工作台
vim ${platform_name}/config/frame_settings.py # 填入配置
bspider master start # 启动master节点第一次启动节点会初始化MySQL表
bspider agent start # 初次启动agent需要使用命令行进行启动，后续可在bspider-studio进行管理
```
> notice:
> 1. bspider-studio默认账号：admin 密码：admin
> 2. 登录地址 http://${frame_settings.MASTER.ip}:{frame_settings.MASTER.port} `此处建议使用默认配置并配置nginx进行端口转发`
> * 单节点下推荐AGENT.ip、MASTER.ip 都使用127.0.0.1

开发文档
========
初始化项目
```shell script
# 在要进行开发的电脑上
bspider startplatform ${platform_name} # 初始化工作台
vim ${platform_name}/config/frame_settings.py # 填入配置 AGENT配置可不填，其他配置和线上配置保持一致
bspider startspider ${spider_name} # 自动生成模板代码
```
开始开发
> 1. *_pipeline.py 类似于Scrapy 的pipeline `一个py文件只能包含一个pipeline class 且类名必须为 *Pipeline`
> 2. *_extractor.py 抽取逻辑。目前`只支持xpath`
> 3. *_middleware.py 下载器中间件。
> 4. settings.json 当前下载任务的配置
> 5. *_task.py 定时任务，用于向队列中推送初始url, 相当于scrapy的start_url

`notice: 每个项目只可配置一个extractor， 但可配置多个pipeline 或 middleware` 

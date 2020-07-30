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

BSpider [Demo](http://bspider-demo.baishanglin.top/)
是一个纯Python实现的高等级分布式全异步web抓取框架，框架采用多进程 + 
协程的方式规避 GIL锁带来的不良影响，充分利用多核CPU性能，同时框架设计上尽可能的
减少框架自身对系统性能的影响，使尽可能多的计算资源用于抓取、解析操作。

特色
========
* 弹性，方便拓展。随时启停工作节点
* pipeline、middleware模块多任务可复用
* webUI, 轻松管理大量复杂抓取任务, 快速发现、解决、处理抓取问题。
* RBAC权限控制。RESTful 风格API, 方便二次开发
* 敏捷开发、调试方便、快速上线

前置依赖
============

* Python 3.7+
* 框架服务只能部署在 Linux, Mac OSX 系统
* 可以在 Linux, Windows, Mac OSX 系统进行开发
* rabbitmq `>3.7.x` 并启用 `rabbitmq management plugins` 提供有访问UI权限的账号
* MySQL `>5.x`

安装
=======

快速安装:

    pip install bspider

或从此git仓库自行安装

## 部署服务
=============
### 多节点部署
启动master
```shell script
bspider mkplatform ${platform_name} # 初始化工作台
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

快速开始
========
初始化项目
```shell script
# 在要进行开发的电脑上
bspider mkplatform ${platform_name} # 初始化工作台
vim ${platform_name}/config/frame_settings.py # 填入配置 AGENT配置可不填，其他配置和线上配置保持一致
bspider mkspider ${spider_name} # 自动生成模板代码
cd ${platform_name}/projects/${spider_name}
# 开始开发
```
各文件说明
> 1. pipeline.*_pipeline.py 类似于Scrapy 的pipeline `一个py文件只能包含一个pipeline class 且类名必须为 *Pipeline`
> 2. project.${project_name}.*_extractor.py 抽取逻辑。目前`只支持xpath 通常一个抓取任务只需编写此组件`
> 3. middleware.*_middleware.py 下载器中间件。`一个py文件只能包含一个middleware class 且类名必须为 *Middleware`
> 4. project.${project_name}.settings.yml 当前下载任务的配置

> 只需编写 extractor 和 yml 配置文件即可完成爬虫开发

`notice: 每个项目只可配置一个extractor， 但可配置多个pipeline 或 middleware` 


发布到服务

*** 发布前先确认有 一个或以上的 parser、downloader `进程`运行
> 进入ui提交任务

TODO

2. 前端权限校验 worker 只能修改自己的 job
4. code 增加 doc 使用文档
5. project页面直达 extractor编辑页面
# bspider

#### 介绍 -v 0.1.23 beta
分布式、高可用的抓取框架

#### 软件架构
参考scrapy、pyspider、k8s设计的一款高可用抓取框架
依赖如下组件: rabbitmq、mysql、sqlite


#### 安装教程

1. pip install bspider
2. 修改config.frame_settings.py 配置
3. 在projects文件夹下进行开发、调试
5. bspider master start|stop 启动停止master节点
6. bspider agent start|stop 启动停止work节点
7. 登录web ui 启动停止 parser、downloader进程

#### 使用说明

1. bspider startplatform xxx 创建工作台
2. 本框架可在win/mac/linux 下进行开发
3. 本框架只可在mac/linux 下进行部署，不支持在win下进行部署
***

#### 参与贡献
1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

#### TODO
* 初次安装自动建表
* agent.node返回值、逻辑优化。节点状态返回优化 done
* master.node逻辑优化、mixin方法优化
* frame_settings supervisor注释优化 done
* debug队列改为优先队列 done
* 接口支持表单 done
* 每个资源增加分页、搜索接口 done
* User 增加创建时间、修改时间返回、修复total参数显示不正确bug done
* web全线放弃 使用xx_name 全部使用 xx_id进行通信 done
* 强化校验 \*Pipeline、\*Task、\*Operation、\*Middleware、\.Extractor
  1. 取出文档所有类->根据名称校验父类->判断父类合规的数量是否为1->通过校验 done
  2. 原有预执行检测也放入校验类、返回 (bool, check_report) done




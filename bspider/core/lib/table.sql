SET FOREIGN_KEY_CHECKS = 0;

DROP table if exists bspider_cronjob;
CREATE TABLE `bspider_cronjob` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `project_id` int(10) NOT NULL COMMENT 'project_id',
  `project_name` varchar(30) NOT NULL COMMENT '定时任务所属的任务名称',
  `class_name` varchar(30) NOT NULL COMMENT '定时任务调用的脚本类名',
  `args` text COMMENT '定时任务需要传入的参数 json.list',
  `kwargs` text COMMENT '定时任务需要传入的参数 json.dict',
  `trigger` text NOT NULL COMMENT '定时任务执行间隔支持crontab写法',
  `trigger_type` varchar(10) NOT NULL COMMENT '定时任务执行间隔类别 cron ...',
  `next_run_time` double DEFAULT NULL COMMENT '任务的下次执行时间',
  `func` text NOT NULL COMMENT '实际执行时调用的方法名称',
  `executor` varchar(10) NOT NULL COMMENT '选择执行者，默认是通过线程池执行',
  `status` int(11) NOT NULL COMMENT '内部任务状态 0无操作任务，1需新增的任务，2需更新的任务，3需删除的任务',
  `description` text NOT NULL COMMENT '当前定时任务的说明文字',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_project_name_class_name` (`project_name`,`class_name`),
  KEY `idx_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_customcode;
CREATE TABLE `bspider_customcode` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `name` varchar(100) NOT NULL COMMENT '方法类名',
  `description` longtext NOT NULL COMMENT '代码功能的简要介绍',
  `type` varchar(100) NOT NULL COMMENT 'operation, pipline, task, middleware',
  `content` longtext NOT NULL COMMENT '代码文本',
  `editor` varchar(50) NOT NULL COMMENT '代码editor',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_project;
CREATE TABLE `bspider_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `name` varchar(100) NOT NULL COMMENT '任务名称',
  `status` int(11) NOT NULL COMMENT '任务状态 0: 关闭 1: 开启 -1: 删除',
  `type` varchar(100) NOT NULL COMMENT '任务种类，operation, crawl',
  `group` varchar(100) NOT NULL COMMENT '业务方向分组, 分为 竞品、线索、抓取支持、车型',
  `description` longtext NOT NULL COMMENT '代码功能的简要介绍',
  `editor` varchar(50) NOT NULL COMMENT '任务editor',
  `rate` double NOT NULL COMMENT '抓取速度 /min',
  `config` longtext COMMENT '配置',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_project_customcode;
CREATE TABLE `bspider_project_customcode` (
  `project_id` int(11) NOT NULL COMMENT '工程id',
  `customcode_id` int(11) NOT NULL COMMENT '代码id',
  PRIMARY KEY (`project_id`,`customcode_id`),
  KEY `customcode_id` (`customcode_id`),
  CONSTRAINT `bspider_project_customcode_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `bspider_project` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bspider_project_customcode_ibfk_2` FOREIGN KEY (`customcode_id`) REFERENCES `bspider_customcode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;


DROP table if exists bspider_user;
CREATE TABLE `bspider_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `identity` varchar(50) NOT NULL COMMENT '身份ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `role` varchar(20) NOT NULL COMMENT '用户角色 admin, work, rd, anonymous',
  `email` varchar(20) DEFAULT NULL COMMENT 'email',
  `phone` varchar(20) DEFAULT NULL COMMENT 'phone',
  `status` int(2) DEFAULT '1' COMMENT '用户状态',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_identity` (`identity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP table if exists bspider_casbin_auth;
CREATE TABLE `bspider_casbin_auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ptype` varchar(10) NOT NULL COMMENT '用户角色',
  `v0` varchar(20) DEFAULT NULL COMMENT '用户名称',
  `v1` varchar(20) DEFAULT NULL,
  `v2` varchar(20) DEFAULT NULL,
  `v3` varchar(20) DEFAULT NULL,
  `v4` varchar(20) DEFAULT NULL,
  `v5` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_downloader_status;
CREATE TABLE `bspider_downloader_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `project_name` varchar(100) NOT NULL COMMENT '任务名称',
  `sign` varchar(150) NOT NULL COMMENT 'request唯一标识',
  `method` varchar(10) NOT NULL COMMENT '请求方法',
  `data` text COMMENT '请求携带参数',
  `url` text NOT NULL COMMENT '请求url',
  `status` int(4) NOT NULL COMMENT '下载状态',
  `url_sign` char(32) NOT NULL COMMENT 'url标识',
  `exception` text COMMENT '异常',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_project_name` (`project_name`),
  KEY `idx_url_sign` (`url_sign`),
  KEY `idx_sign` (`sign`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_parser_status;
CREATE TABLE `bspider_parser_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `project_name` varchar(100) NOT NULL COMMENT '任务名称',
  `sign` varchar(150) NOT NULL COMMENT 'request唯一标识',
  `method` varchar(10) NOT NULL COMMENT '请求方法',
  `data` text COMMENT '请求携带参数',
  `url` text NOT NULL COMMENT '请求url',
  `status` int(4) NOT NULL COMMENT '下载状态',
  `url_sign` char(32) NOT NULL COMMENT 'url标识',
  `exception` text COMMENT '异常',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_project_name` (`project_name`),
  KEY `idx_url_sign` (`url_sign`),
  KEY `idx_sign` (`sign`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_node;
CREATE TABLE `bspider_node` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ip` varchar(50) NOT NULL COMMENT '节点ip(内网)',
  `name` varchar(50) NOT NULL COMMENT '节点名称',
  `description` text NOT NULL COMMENT '节点简介',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_ip` (`ip`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_worker;
CREATE TABLE `bspider_worker` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ip` varchar(50) NOT NULL COMMENT 'work 所属节点ip',
  `name` varchar(50) NOT NULL COMMENT 'worker 名称',
  `type` varchar(15) NOT NULL COMMENT 'worker 种类 downloader parser',
  `description` text NOT NULL COMMENT 'worker 介绍',
  `status` int(4) NOT NULL COMMENT 'worker状态 0关闭 1启动 -1异常',
  `coroutine_num` int(4) NOT NULL COMMENT 'worker 使用的协程数量',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_ip` (`ip`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_node_status;
CREATE TABLE `bspider_node_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ip` varchar(50) NOT NULL COMMENT '节点ip(内网)',
  `memory` int(4) NOT NULL COMMENT '节点内存',
  `cpu` int(4) NOT NULL COMMENT 'CPU占用',
  `disk` int(4) NOT NULL COMMENT '磁盘占用',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_ict` (`ip`,`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_worker_status;
CREATE TABLE `bspider_worker_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `worker_sign` varchar(50) NOT NULL COMMENT '{unique_sign}:{worker_type}:{ip}',
  `memory` int(4) NOT NULL COMMENT '节点内存',
  `cpu` int(4) NOT NULL COMMENT 'CPU占用',
  `disk` int(4) NOT NULL COMMENT '磁盘占用',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_wsct` (`worker_sign`,`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

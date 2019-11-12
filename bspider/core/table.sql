
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

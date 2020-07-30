SET FOREIGN_KEY_CHECKS = 0;

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
  `r_config` longtext COMMENT '转义后的配置，用于同步给工作节点进行缓存',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
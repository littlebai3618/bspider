SET FOREIGN_KEY_CHECKS = 0;

DROP table if exists bspider_data_source;
CREATE TABLE `bspider_data_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `name` varchar(50) NOT NULL COMMENT '数据源名称',
  `type` varchar(10) NOT NULL COMMENT '数据源类型',
  `param` text NOT NULL COMMENT '连接参数 json dict',
  `status` int(2) NOT NULL COMMENT '数据源状态 用于测试集群是否可以访问目标数据源 0 失败 1 成功',
  `description` text NOT NULL COMMENT '当前定时任务的说明文字',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`),
  KEY `idx_type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
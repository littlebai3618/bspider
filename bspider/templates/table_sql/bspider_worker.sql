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
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
DROP table if exists bspider_node;
CREATE TABLE `bspider_node` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ip` varchar(50) NOT NULL COMMENT '节点ip(内网)',
  `port` int(7) NOT NULL COMMENT '节点AGENT占用端口',
  `name` varchar(50) NOT NULL COMMENT '节点名称',
  `cpu_num` int(2) NOT NULL COMMENT 'cpu数量 逻辑核心',
  `mem_size` float(5, 2) NOT NULL COMMENT '内存大小 GB',
  `disk_size` float(11, 2) NOT NULL COMMENT '硬盘大小 GB',
  `status` int(11) NOT NULL COMMENT '节点状态 0: 关闭 1: 开启 -1: 异常',
  `description` text NOT NULL COMMENT '节点简介',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_ip` (`ip`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
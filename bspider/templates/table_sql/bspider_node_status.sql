DROP table if exists bspider_node_status;
CREATE TABLE `bspider_node_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ip` varchar(50) NOT NULL COMMENT '节点ip(内网)',
  `memory` float(5,2) NOT NULL COMMENT '节点内存',
  `cpu` float(5,2) NOT NULL COMMENT 'CPU占用',
  `disk` float(5,2) NOT NULL COMMENT '磁盘占用',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_ict` (`ip`,`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
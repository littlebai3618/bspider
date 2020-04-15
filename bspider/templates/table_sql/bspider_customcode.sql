SET FOREIGN_KEY_CHECKS = 0;

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

SET FOREIGN_KEY_CHECKS = 1;

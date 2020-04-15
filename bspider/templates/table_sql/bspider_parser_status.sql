DROP table if exists bspider_parser_status;
CREATE TABLE `bspider_parser_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `project_id` int(11) NOT NULL COMMENT '任务id',
  `project_name` varchar(100) NOT NULL COMMENT '任务名称',
  `sign` varchar(150) NOT NULL COMMENT 'request唯一标识',
  `method` varchar(10) NOT NULL COMMENT '请求方法',
  `data` text COMMENT '请求携带参数',
  `url` text NOT NULL COMMENT '请求url',
  `status` int(4) NOT NULL COMMENT '下载状态',
  `url_sign` char(32) NOT NULL COMMENT 'url标识',
  `exception` text COMMENT '异常',
  `response` text COMMENT 'response',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_project_id` (`project_id`),
  KEY `idx_project_name` (`project_name`),
  KEY `idx_url_sign` (`url_sign`),
  KEY `idx_sign` (`sign`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
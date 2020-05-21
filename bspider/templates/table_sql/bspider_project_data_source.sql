SET FOREIGN_KEY_CHECKS = 0;

DROP table if exists bspider_project_data_source;
CREATE TABLE `bspider_project_data_source` (
  `project_id` int(11) NOT NULL COMMENT '工程id',
  `data_source_id` int(11) NOT NULL COMMENT '代码id',
  PRIMARY KEY (`project_id`,`data_source_id`),
  KEY `idx_data_source_id` (`data_source_id`),
  KEY `idx_project_id` (`project_id`),
  CONSTRAINT `bspider_project_data_source_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `bspider_project` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bspider_project_data_source_ibfk_2` FOREIGN KEY (`data_source_id`) REFERENCES `bspider_data_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
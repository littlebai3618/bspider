SET FOREIGN_KEY_CHECKS = 0;

DROP table if exists bspider_project_customcode;
CREATE TABLE `bspider_project_customcode` (
  `project_id` int(11) NOT NULL COMMENT '工程id',
  `customcode_id` int(11) NOT NULL COMMENT '代码id',
  PRIMARY KEY (`project_id`,`customcode_id`),
  KEY `customcode_id` (`customcode_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `bspider_project_customcode_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `bspider_project` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bspider_project_customcode_ibfk_2` FOREIGN KEY (`customcode_id`) REFERENCES `bspider_customcode` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
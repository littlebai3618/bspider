SET FOREIGN_KEY_CHECKS = 0;

-- DROP table if exists bspider_cronjob;
-- CREATE TABLE `bspider_cronjob` (
--   `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
--   `project_id` int(10) NOT NULL COMMENT 'project_id',
--   `project_name` varchar(30) NOT NULL COMMENT '定时任务所属的任务名称',
--   `class_name` varchar(30) NOT NULL COMMENT '定时任务调用的脚本类名',
--   `args` text COMMENT '定时任务需要传入的参数 json.list',
--   `kwargs` text COMMENT '定时任务需要传入的参数 json.dict',
--   `trigger` text NOT NULL COMMENT '定时任务执行间隔支持crontab写法',
--   `trigger_type` varchar(10) NOT NULL COMMENT '定时任务执行间隔类别 cron ...',
--   `next_run_time` double DEFAULT NULL COMMENT '任务的下次执行时间',
--   `func` text NOT NULL COMMENT '实际执行时调用的方法名称',
--   `executor` varchar(10) NOT NULL COMMENT '选择执行者，默认是通过线程池执行',
--   `status` int(11) NOT NULL COMMENT '内部任务状态 0无操作任务，1需新增的任务，2需更新的任务，3需删除的任务',
--   `description` text NOT NULL COMMENT '当前定时任务的说明文字',
--   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
--   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `idx_project_name_class_name` (`project_name`,`class_name`),
--   KEY `idx_next_run_time` (`next_run_time`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP table if exists bspider_cron;
CREATE TABLE `bspider_cron` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `project_id` int(10) NOT NULL COMMENT 'project_id',
  `code_id` int(10) NOT NULL COMMENT 'code_id',
  `type` varchar(10) NOT NULL COMMENT 'spider、 operation',
  `trigger` text NOT NULL COMMENT '定时任务执行间隔支持crontab写法',
  `trigger_type` varchar(10) NOT NULL COMMENT '定时任务执行间隔类别 cron ...',
  `next_run_time` double DEFAULT NULL COMMENT '任务的下次执行时间',
  `func` text NOT NULL COMMENT '实际执行时调用的方法名称',
  `executor` varchar(20) NOT NULL COMMENT '选择执行者，默认是通过线程池执行',
  `status` int(2) NOT NULL COMMENT '内部任务状态 0无操作任务，1需新增的任务，2需更新的任务，3需删除的任务',
  `description` text NOT NULL COMMENT '当前定时任务的说明文字',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_project_code_id` (`project_id`,`code_id`),
  KEY `idx_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

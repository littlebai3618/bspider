DROP table if exists bspider_casbin_auth;
CREATE TABLE `bspider_casbin_auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ptype` varchar(10) NOT NULL COMMENT '用户角色',
  `v0` varchar(20) DEFAULT NULL COMMENT '用户名称',
  `v1` varchar(20) DEFAULT NULL,
  `v2` varchar(20) DEFAULT NULL,
  `v3` varchar(20) DEFAULT NULL,
  `v4` varchar(20) DEFAULT NULL,
  `v5` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
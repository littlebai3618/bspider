DROP table if exists bspider_user;
CREATE TABLE `bspider_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `identity` varchar(50) NOT NULL COMMENT '身份ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `role` varchar(20) NOT NULL COMMENT '用户角色 admin, work, read',
  `email` varchar(20) DEFAULT NULL COMMENT 'email',
  `phone` varchar(20) DEFAULT NULL COMMENT 'phone',
  `status` int(2) DEFAULT 1 COMMENT '用户状态 1 正常 0 关闭',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_identity` (`identity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `bspider_user`(`identity`, `username`, `password`, `role`, `status`) VALUES ('admin', 'admin', '${password}', 'admin', 1);
INSERT INTO `bspider_user`(`identity`, `username`, `password`, `role`, `status`) VALUES ('operation', 'operation', '${password}', 'operation', 1);
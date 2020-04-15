from bspider.core.api import BaseImpl
from bspider.master import log


class ChartImpl(BaseImpl):

    def get_project_downloader_pv(self, project_id: int = None):
        """获取按小时统计的下载数据"""
        if project_id:
            sql = f"SELECT DATE_FORMAT(`create_time`,'%Y-%m-%d %H:00:00') AS `time`," \
                  f"COUNT(IF (`status` !=200,TRUE,NULL)) AS `exception`," \
                  f"COUNT(*) AS total " \
                  f"FROM {self.downloader_status_table} " \
                  f"WHERE `project_id`={project_id} " \
                  f"GROUP BY `time` ORDER BY `time`;"
        else:
            sql = f"SELECT DATE_FORMAT(`create_time`,'%Y-%m-%d %H:00:00') AS `time`," \
                  f"COUNT(IF (`status` !=200,TRUE,NULL)) AS `exception`," \
                  f"COUNT(*) AS total " \
                  f"FROM {self.downloader_status_table} " \
                  f"GROUP BY `time` ORDER BY `time`;"
        return self.mysql_client.select(sql)

    def get_project_parser_pv(self, project_id: int = None):
        if project_id:
            sql = f"SELECT DATE_FORMAT(`create_time`,'%Y-%m-%d %H:00:00') AS `time`," \
                  f"COUNT(IF (`exception` is not null,TRUE,NULL)) AS `exception`," \
                  f"COUNT(*) AS total " \
                  f"FROM {self.parser_status_table} " \
                  f"WHERE `project_id`={project_id} " \
                  f"GROUP BY `time` ORDER BY `time`;"
        else:
            sql = f"SELECT DATE_FORMAT(`create_time`,'%Y-%m-%d %H:00:00') AS `time`," \
                  f"COUNT(IF (`exception` is not null,TRUE,NULL)) AS `exception`," \
                  f"COUNT(*) AS total " \
                  f"FROM {self.parser_status_table} " \
                  f"GROUP BY `time` ORDER BY `time`;"
        return self.mysql_client.select(sql)

    def get_code_type_detail(self):
        sql = f'select count(1) as `value`, `type` as `name` from {self.code_table} GROUP BY `type`'
        return self.mysql_client.select(sql)

    def get_node_pv(self, node_ip: str = None):
        """获取按小时统计的下载数据"""
        sql = f"SELECT DATE_FORMAT(`create_time`,'%Y-%m-%d %H:00:00') AS `time`," \
              f"avg(`memory`) as `memory`," \
              f"avg(`cpu`) as `cpu`, " \
              f"avg(`disk`) as `disk` " \
              f"FROM {self.node_status_table} " \
              f"WHERE `ip`='{node_ip}' " \
              f"GROUP BY `time` ORDER BY `time`;"
        log.debug(sql)
        return self.mysql_client.select(sql)

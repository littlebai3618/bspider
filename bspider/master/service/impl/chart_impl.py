# @Time    : 2019/7/11 6:55 PM
# @Author  : 白尚林
# @File    : tools_impl
# @Use     :
from bspider.core.api import BaseImpl


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
        return self.handler.select(sql)

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
        return self.handler.select(sql)

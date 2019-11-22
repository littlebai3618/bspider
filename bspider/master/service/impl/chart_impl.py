# @Time    : 2019/7/11 6:55 PM
# @Author  : 白尚林
# @File    : tools_impl
# @Use     :
from bspider.core.api import BaseImpl


class ChartImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.node_table = self.frame_settings['NODE_TABLE']
        self.code_table = self.frame_settings['CODE_STORE_TABLE']
        self.downloader_status_table  = self.frame_settings['DOWNLOADER_STATUS_TABLE']
        self.parser_status_table = self.frame_settings['PARSER_STATUS_TABLE']

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


    # def get_downloader_error(self, project_name):
    #     """目前是自动获取8小时内，前4条错误信息"""
    #     sql = f'SELECT `project_name`,`sign`,`method`,`data` ,`url`,`status`,`url_sign`,' \
    #           f'`exception`,`create_time` as crawl_time ' \
    #           f'FROM {self.downloader_status_table} ' \
    #           f'WHERE create_time > now()-INTERVAL 8 HOUR ' \
    #           f'AND project_name="{project_name}" ' \
    #           f'AND `status` NOT BETWEEN 900 AND 999 ' \
    #           f'AND `status` !=200 ' \
    #           f'GROUP BY `exception` ORDER BY `create_time` DESC LIMIT 4'
    #     return self.handler.select(sql)
    #
    # def get_parser_error(self, project_name):
    #     sql = f'SELECT `project_name`,`sign`,`method`,`data` ,`url`,`status`,`url_sign`,' \
    #           f'`exception`,`create_time` as crawl_time ' \
    #           f'FROM {self.parser_status_table} ' \
    #           f'WHERE create_time > now()-INTERVAL 8 HOUR ' \
    #           f'AND project_name="{project_name}" ' \
    #           f'AND `status`=-1 ' \
    #           f'GROUP BY `exception` ORDER BY `create_time` DESC LIMIT 4'
    #     return self.handler.select(sql)
    #
    # def get_reqest_track(self, sign):
    #     result = {}
    #     sql = f'select `project_name`,`sign`,`method`,`data` ,`url`,`status`,`url_sign`,' \
    #           f'`exception`,`create_time` as crawl_time ' \
    #           f'FROM {self.parser_status_table} ' \
    #           f'WHERE  `sign`="{sign}"'
    #     parser = self.handler.select(sql)
    #     if len(parser):
    #         result['parser'] = parser[0]
    #     sql = f'select `project_name`,`sign`,`method`,`data` ,`url`,`status`,`url_sign`,' \
    #           f'`exception`,`create_time` as crawl_time ' \
    #           f'FROM {self.downloader_status_table} ' \
    #           f'WHERE  `sign`="{sign}"'
    #     downloader = self.handler.select(sql)
    #     if len(downloader):
    #         result['download'] = downloader[0]
    #     return result
    #
    # def get_sign_by_url(self, url):
    #     sql = f'select `sign` from {self.downloader_status_table} ' \
    #           f'where `url_sign`=md5("{url}") ' \
    #           f'ORDER BY `create_time` DESC LIMIT 1'
    #     info = self.handler.select(sql)
    #     if len(info):
    #         return info['sign']

# @Time    : 2019/7/11 6:55 PM
# @Author  : 白尚林
# @File    : tools_impl
# @Use     :
from bspider.core.api import BaseImpl


class ToolsImpl(BaseImpl):

    def __init__(self):
        super().__init__()
        self.node_table = self.frame_settings['NODE_TABLE']
        self.code_table = self.frame_settings['CODE_STORE_TABLE']
        self.downloader_status_table  = self.frame_settings['DOWNLOADER_STATUS_TABLE']
        self.parser_status_table = self.frame_settings['PARSER_STATUS_TABLE']

    def get_node_list(self):
        sql = f"select `id`, `name`, `ip` from `{self.node_table}`;"
        return self.handler.select(sql)

    def get_code_list(self, code_type):
        if code_type:
            sql = f"select `id`, `name`, `editor` from `{self.code_table}` where `type`='{code_type}';"
        else:
            sql = f"select `id`, `name`, `editor` from `{self.code_table}`;"
        return self.handler.select(sql)


    def get_downloader_exception(self, project_id):
        """目前是自动获取8小时内，前4条错误信息"""
        sql = f'SELECT `project_id`, `project_name`,`sign`,`method`,`data` ,`url`,`status`,`url_sign`,' \
              f'`exception`,`create_time` as crawl_time ' \
              f'FROM {self.downloader_status_table} ' \
              f'WHERE `create_time` > now()-INTERVAL 8 HOUR ' \
              f'AND `project_id`="{project_id}" ' \
              f'AND `status` NOT BETWEEN 900 AND 999 ' \
              f'AND `status` !=200 ' \
              f'GROUP BY `exception` ORDER BY `create_time` DESC LIMIT 4'
        return self.handler.select(sql)

    def get_parser_exception(self, project_id):
        sql = f'SELECT `project_name`,`sign`,`method`,`data` ,`url`,`status`,`url_sign`,' \
              f'`exception`,`create_time` as crawl_time ' \
              f'FROM {self.parser_status_table} ' \
              f'WHERE `create_time` > now()-INTERVAL 8 HOUR ' \
              f'AND `project_id`="{project_id}" ' \
              f'AND `exception` is not null ' \
              f'GROUP BY `exception` ORDER BY `create_time` DESC LIMIT 4'
        return self.handler.select(sql)
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

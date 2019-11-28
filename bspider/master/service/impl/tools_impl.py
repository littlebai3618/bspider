# @Time    : 2019/7/11 6:55 PM
# @Author  : 白尚林
# @File    : tools_impl
# @Use     :
from bspider.core.api import BaseImpl
from bspider.master import log


class ToolsImpl(BaseImpl):

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
        sql = f'SELECT `sign`,`method`, `url`, `status`, `url_sign`,' \
              f'`exception`,`create_time` as crawl_time ' \
              f'FROM {self.downloader_status_table} ' \
              f'WHERE `create_time` > now()-INTERVAL 8 HOUR ' \
              f'AND `project_id`="{project_id}" ' \
              f'AND `status` NOT BETWEEN 900 AND 999 ' \
              f'AND `status` !=200 ' \
              f'ORDER BY `create_time` DESC LIMIT 4'
        return self.handler.select(sql)

    def get_parser_exception(self, project_id):
        sql = f'SELECT `sign`,`method`,`url`,`status`,`url_sign`,' \
              f'`exception`,`create_time` as crawl_time ' \
              f'FROM {self.parser_status_table} ' \
              f'WHERE `create_time` > now()-INTERVAL 8 HOUR ' \
              f'AND `project_id`="{project_id}" ' \
              f'AND `exception` is not null ' \
              f'GROUP BY `exception` ORDER BY `create_time` DESC LIMIT 4'
        return self.handler.select(sql)

    def get_crawl_detail(self, value, source):
        if source == 'parser':
            table = self.parser_status_table
        else:
            table = self.downloader_status_table

        sql = f'select `project_id`, `project_name`,`sign`,`method`,`data` ,`url`,`status`,`url_sign`,`response`,' \
              f'`exception`,`create_time` as crawl_time ' \
              f'FROM {table} ' \
              f'WHERE  `sign`="{value}"'

        return self.handler.select(sql)

    def get_sign_by_url(self, url):
        sql = f'select `sign` from {self.downloader_status_table} ' \
              f'where `url_sign`=md5("{url}") ' \
              f'ORDER BY `create_time` DESC LIMIT 1'
        info = self.handler.select(sql)
        if len(info):
            log.info('url:{} -> sign:{}'.format(url, info[0]['sign']))
            return info[0]['sign']
        log.info(f'can\'t find url:{url} sign')

    def get_node_detail(self):
        sql = f'SELECT count(1) AS `node`,' \
              f'SUM(`mem_size`) AS `memory`, ' \
              f'SUM(`disk_size`) AS `disk`, ' \
              f'convert(SUM(`cpu_num`), signed) AS `cpu` ' \
              f'from {self.node_table} where `status`=1'
        return self.handler.select(sql)

    def get_exception_project(self):
        sql = f'select `id`, `name`, `editor`, `rate`, `status` from {self.project_table} where `status` = -1'
        return self.handler.select(sql)

    def get_code_type_detail(self):
        sql = f'select count(1) as `value`, `type` as `name` from {self.code_table} GROUP BY `type`'
        return self.handler.select(sql)


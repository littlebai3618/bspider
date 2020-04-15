from bspider.core.api import BaseImpl
from bspider.master import log


class ToolsImpl(BaseImpl):

    def get_node_list(self):
        sql = f"select `id`, `name`, `ip` from `{self.node_table}`;"
        return self.mysql_client.select(sql)

    def get_code_list(self, code_type):
        if code_type:
            sql = f"select `id`, `name`, `editor` from `{self.code_table}` where `type`='{code_type}';"
        else:
            sql = f"select `id`, `name`, `editor` from `{self.code_table}`;"
        return self.mysql_client.select(sql)


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
        return self.mysql_client.select(sql)

    def get_parser_exception(self, project_id):
        sql = f'SELECT `sign`,`method`,`url`,`status`,`url_sign`,' \
              f'`exception`,`create_time` as crawl_time ' \
              f'FROM {self.parser_status_table} ' \
              f'WHERE `create_time` > now()-INTERVAL 8 HOUR ' \
              f'AND `project_id`="{project_id}" ' \
              f'AND `exception` is not null ' \
              f'GROUP BY `exception` ORDER BY `create_time` DESC LIMIT 4'
        return self.mysql_client.select(sql)

    def get_crawl_detail(self, value, source):
        if source == 'parser':
            table = self.parser_status_table
        else:
            table = self.downloader_status_table

        sql = f'select `project_id`, `project_name`,`sign`,`method`,`data` ,`url`,`status`,`url_sign`,`response`,' \
              f'`exception`,`create_time` as crawl_time ' \
              f'FROM {table} ' \
              f'WHERE  `sign`="{value}"'

        return self.mysql_client.select(sql)

    def get_sign_by_url(self, url):
        sql = f'select `sign` from {self.downloader_status_table} ' \
              f'where `url_sign`=md5("{url}") ' \
              f'ORDER BY `create_time` DESC LIMIT 1'
        info = self.mysql_client.select(sql)
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
        return self.mysql_client.select(sql)

    def get_exception_project(self):
        sql = f'select `id`, `name`, `editor`, `rate`, `status` from {self.project_table} where `status` = -1'
        return self.mysql_client.select(sql)

    def get_user_by_id(self, id):
        """暂时先这样，后面增加复杂密码验证"""
        sql = f'select `id`, `identity`, `username`, `role`, `email`, `phone`, `status`, `create_time`, `update_time`  ' \
              f'from {self.user_table} where `id`=%s;'
        return self.mysql_client.select(sql, id)


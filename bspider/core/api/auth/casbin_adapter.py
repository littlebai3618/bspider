# @Time    : 2019/6/20 11:39 AM
# @Author  : 白尚林
# @File    : casbin_adapter
# @Use     :
from casbin.persist import Adapter, load_policy_line
from flask.logging import default_handler as log

from bspider.utils.database.mysql import MysqlHandler
from bspider.config import FrameSettings


class MySQLAdapter(Adapter):
    """the interface for Casbin adapters."""

    def __init__(self):
        self.frame_settings = FrameSettings()
        self.handler = MysqlHandler.from_settings(self.frame_settings['WEB_STUDIO_DB'])
        self.table_name = self.frame_settings['AUTH_RULE_TABLE']

    def load_policy(self, model):
        """loads all policy rules from the storage."""
        sql = f'select `ptype`, `v0`, `v1`,`v2`,`v3`,`v4`,`v5` from {self.table_name}'
        lines = self.handler.select(sql)
        for line in lines:
            value = '{ptype}, {v0}, {v1}, {v2}, {v3}, {v4}, {v5}'.format(**line)
            load_policy_line(value, model)

    def _save_policy_line(self, ptype, rule):
        fields, values = self.make_fv(ptype, rule)
        sql = f"insert into {self.table_name} set {fields}"
        result = self.handler.insert(sql, values)
        if result:
            log.info('success add a new policy:{}'.format(values))
        else:
            log.error('failed add a new policy:{}'.format(values))


    def save_policy(self, model):
        """saves all policy rules to the storage."""
        for sec in ["p", "g"]:
            if sec not in model.model.keys():
                continue
            for ptype, ast in model.model[sec].items():
                for rule in ast.policy:
                    self._save_policy_line(ptype, rule)
        return True

    def add_policy(self, sec, ptype, rule):
        """adds a policy rule to the storage."""
        self._save_policy_line(ptype, rule)

    def remove_policy(self, sec, ptype, rule):
        """removes a policy rule from the storage."""
        fields, values = self.make_fv(ptype, rule)
        sql = f'delete from {self.table_name} where {fields}'
        if self.handler.delete(sql, values):
            return True

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """removes policy rules that match the filter from the storage.
        This is part of the Auto-Save feature.
        """
        return False

    @staticmethod
    def make_fv(ptype: str, rule: list) -> tuple:
        data = {'ptype': ptype}
        if len(rule) > 0:
            data['v0'] = rule[0]
        if len(rule) > 1:
            data['v1'] = rule[1]
        if len(rule) > 2:
            data['v2'] = rule[2]
        if len(rule) > 3:
            data['v3'] = rule[3]
        if len(rule) > 4:
            data['v4'] = rule[4]
        if len(rule) > 5:
            data['v5'] = rule[5]
        fields = ','.join([' `%s`=%%s ' % (key) for key in data.keys() if data.get(key)])
        values = [data[key] for key in data.keys() if data.get(key)]

        return fields, values

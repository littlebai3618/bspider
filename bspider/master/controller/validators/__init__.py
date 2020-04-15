from wtforms import StringField, IntegerField

from bspider.core.api import BaseForm


class PageForm(BaseForm):
    """分页参数"""
    page = IntegerField(default=1)
    limit = IntegerField(default=8)
    search = StringField(default='')
    sort = StringField(default='DESC')

    def validate_page(self, value):
        self.__to_int(value)

    def validate_limit(self, value):
        self.__to_int(value)

    def __to_int(self, value):
        try:
            value.data = int(value.data)
        except ValueError as e:
            raise e


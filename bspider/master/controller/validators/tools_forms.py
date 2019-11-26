# @Time    : 2019-08-01 15:26
# @Author  : 白尚林
# @File    : forms
# @Use     :
from enum import Enum
from wtforms import StringField, IntegerField

from bspider.core.api import BaseForm, ParamRequired


class GetCodeListForm(BaseForm):
    type = StringField()


class ValidateForm(BaseForm):
    data = StringField(validators=[ParamRequired()])


class CrawlDetailTagEnum(Enum):
    sign = 'sign'
    url = 'url'


class GetCrawlDetailForm(BaseForm):
    tag = StringField(validators=[ParamRequired()])
    data = StringField(validators=[ParamRequired()])

    def validate_tag(self, value):
        try:
            value.data = CrawlDetailTagEnum(value.data).name
        except ValueError as e:
            raise e

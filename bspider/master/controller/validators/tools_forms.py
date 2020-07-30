from enum import Enum
from wtforms import StringField

from bspider.core.api import BaseForm, ParamRequired


class GetCodeListForm(BaseForm):
    type = StringField()


class ValidateForm(BaseForm):
    data = StringField(validators=[ParamRequired()])


class CrawlDetailTagEnum(Enum):
    sign = 'sign'
    url = 'url'


class CrawlDetailSourceEnum(Enum):
    parser = 'parser'
    downloader = 'downloader'


class GetCrawlDetailForm(BaseForm):
    tag = StringField(validators=[ParamRequired()])
    data = StringField(validators=[ParamRequired()])
    source = StringField(validators=[ParamRequired()])

    def validate_tag(self, value):
        try:
            value.data = CrawlDetailTagEnum(value.data).name
        except ValueError as e:
            raise e

    def validate_source(self, value):
        try:
            value.data = CrawlDetailSourceEnum(value.data).name
        except ValueError as e:
            raise e

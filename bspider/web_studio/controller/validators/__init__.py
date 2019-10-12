# @Time    : 2019-08-01 15:13
# @Author  : 白尚林
# @File    : __init__
# @Use     :
from wtforms import StringField

from bspider.core.api import BaseForm, IntegerField


class PageForm(BaseForm):
    """分页参数"""
    page = IntegerField(default=0)
    limit = IntegerField(default=8)
    search = StringField(default='')
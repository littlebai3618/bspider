# @Time    : 2019-08-01 15:26
# @Author  : 白尚林
# @File    : forms
# @Use     :
from wtforms import StringField

from bspider.core.api import BaseForm, ParamRequired


class GetCodeListForm(BaseForm):
    type = StringField()

class ValidateForm(BaseForm):
    data = StringField(validators=[ParamRequired()])

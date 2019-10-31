# @Time    : 2019-08-13 17:35
# @Author  : 白尚林
# @File    : project_form
# @Use     :
from wtforms import IntegerField, StringField

from bspider.core.api import BaseForm, ParamRequired


class AddForm(BaseForm):
    code_id = IntegerField(validators=[ParamRequired()])
    content = StringField(validators=[ParamRequired()])


class UpdateForm(BaseForm):
    content = StringField()

# @Time    : 2019-08-14 17:16
# @Author  : 白尚林
# @File    : code_forms
# @Use     :
from wtforms import StringField

from bspider.core.api import BaseForm, ParamRequired


class AddForm(BaseForm):
    name = StringField(validators=[ParamRequired()])
    description = StringField(validators=[ParamRequired()])
    type = StringField(validators=[ParamRequired()])
    content = StringField(validators=[ParamRequired()])
    editor = StringField(validators=[ParamRequired()])


class UpdateForm(BaseForm):
    name = StringField(validators=[ParamRequired()])
    description = StringField()
    type = StringField()
    content = StringField()
    editor = StringField()

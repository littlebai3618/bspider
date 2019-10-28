# @Time    : 2019-08-14 11:13
# @Author  : 白尚林
# @File    : project_form
# @Use     :
from wtforms import StringField, IntegerField

from bspider.core.api import BaseForm, ParamRequired

class AddForm(BaseForm):
    name = StringField(validators=[ParamRequired()])
    status = IntegerField(default=0)
    type = StringField(default='crawl')
    group = StringField(validators=[ParamRequired()])
    description = StringField(validators=[ParamRequired()])
    editor = StringField(validators=[ParamRequired()])
    rate = StringField(validators=[ParamRequired()])
    config = StringField(validators=[ParamRequired()])

class UpdateForm(BaseForm):
    project_id = StringField(validators=[ParamRequired()])
    name = StringField(validators=[ParamRequired()])
    status = IntegerField()
    type = StringField()
    group = StringField()
    description = StringField()
    editor = StringField()
    rate = StringField()
    config = StringField()
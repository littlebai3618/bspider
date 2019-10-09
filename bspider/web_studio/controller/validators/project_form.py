# @Time    : 2019-08-14 11:13
# @Author  : 白尚林
# @File    : project_form
# @Use     :
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from bspider.core.api import BaseForm

class AddForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    status = IntegerField(default=0)
    type = StringField(default='crawl')
    group = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])
    editor = StringField(validators=[DataRequired()])
    rate = StringField(validators=[DataRequired()])
    config = StringField(validators=[DataRequired()])

class UpdateForm(BaseForm):
    project_id = StringField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    status = IntegerField()
    type = StringField()
    group = StringField()
    description = StringField()
    editor = StringField()
    rate = StringField()
    config = StringField()
from wtforms import StringField, IntegerField

from bspider.core.api import BaseForm, ParamRequired


class AddForm(BaseForm):
    project_id = IntegerField(validators=[ParamRequired()])
    code_id = IntegerField(validators=[ParamRequired()])
    type = StringField(validators=[ParamRequired()])
    trigger = StringField(validators=[ParamRequired()])
    description = StringField(validators=[ParamRequired()])


class UpdateForm(BaseForm):
    project_id = IntegerField()
    code_id = IntegerField()
    type = StringField()
    trigger = StringField()
    description = StringField()

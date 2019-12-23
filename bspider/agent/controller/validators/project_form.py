from wtforms import IntegerField, StringField

from bspider.core.api import BaseForm, ParamRequired


class AddForm(BaseForm):
    project_id = IntegerField(validators=[ParamRequired()])
    name = StringField(validators=[ParamRequired()])
    config = StringField(validators=[ParamRequired()])
    rate = IntegerField(validators=[ParamRequired()])
    status = IntegerField(validators=[ParamRequired()])


class UpdateForm(BaseForm):
    name = StringField()
    config = StringField()
    rate = IntegerField()
    status = IntegerField()

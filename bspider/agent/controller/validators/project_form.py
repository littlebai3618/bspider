# @Time    : 2019-08-13 17:35
# @Author  : 白尚林
# @File    : project_form
# @Use     :

from wtforms import IntegerField, StringField

from bspider.core.api import ParameterException, BaseForm, ParamRequired


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

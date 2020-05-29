import json
from wtforms import StringField

from bspider.core.api import BaseForm, ParamRequired
from bspider.utils.database import invalid_data_source
from bspider.utils.exceptions import DataSourceTypeError


class AddForm(BaseForm):
    name = StringField(validators=[ParamRequired()])
    type = StringField(validators=[ParamRequired()])
    param = StringField(validators=[ParamRequired()])
    description = StringField(validators=[ParamRequired()])

    def validate_param(self, value):
        value.data = json.loads(value.data)

    def validate_type(self, value):
        if value.data not in invalid_data_source:
            raise DataSourceTypeError('Invalid data source type: %s' % (value.data))


class UpdateForm(AddForm):
    param = StringField()
    description = StringField()

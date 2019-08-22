# @Time    : 2019-08-01 15:13
# @Author  : 白尚林
# @File    : base
# @Use     :
from flask import request
from wtforms import Form, IntegerField
from wtforms.compat import string_types
from wtforms.validators import DataRequired, StopValidation

from core.api.exception import ParameterException


class BaseForm(Form):

    def __init__(self):
        tmp = request.args.to_dict()
        if request.json:
            for key, values in request.json.items():
                tmp[key] = values
        super().__init__(data=tmp)
        self.__validate_for_api()

    def __validate_for_api(self):
        if not super().validate():
            raise ParameterException(msg=self.errors)

    def get_dict(self):
        result = {}
        for name, field in self._fields.items():
            if field is not None and field.data is not None:
                result[name] = field.data
        return result


class ParamRequired(DataRequired):
    """修复wtf DataRequired int=0 时识别失败的bug"""
    def __call__(self, form, field):
        if isinstance(field.data, int) and isinstance(field, IntegerField):
            return
        super().__call__(form, field)


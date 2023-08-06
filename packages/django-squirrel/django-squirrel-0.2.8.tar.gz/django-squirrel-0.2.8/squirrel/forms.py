from logging import getLogger as getLocalLogger
from squirrel.fields import FieldBase
import json

logger = getLocalLogger(__name__)


class SortedArgs:
    columns = []

    def sorted_args(self, **inputs) -> list:
        sorted_args = []
        for col in self.columns:
            sorted_args.append(inputs.get(col))
        return sorted_args


class Form(SortedArgs):
    """Form"""

    def __get_all_fields__(self) -> list:
        fields = []
        for m in dir(self):
            if isinstance(getattr(self, m), FieldBase) and not m.startswith('__'):
                fields.append(m)
        return fields

    def __init__(self, **inputs):
        fields = self.__get_all_fields__()
        for field in fields:
            input_value = inputs.get(field)
            _property = getattr(self, field)
            if input_value is not None:
                _property.set(input_value)
            # elif _property.required:
            #     raise ValueError('Field %s is required' % field)

    def to_dict(self) -> dict:
        return {getattr(self, f).field_name: getattr(self, f).get() for f in self.__get_all_fields__()}

    def args(self):
        return self.sorted_args(**self.to_dict())

    def __str__(self):
        return '%s' % json.dumps(self.to_dict(), indent=4)

from squirrel.exceptions import BadRequest, InternalError
from logging import getLogger as getLocalLogger

logger = getLocalLogger(__name__)


class Context:
    """View Context"""

    __vars_list__ = []

    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            for attr, value in kwargs.items():
                setattr(self, attr, value)
        if len(args) > 0:
            self.__vars_list__ = args
        if len(args) + len(kwargs) == 0:
            raise BadRequest(f'Invalid context. args: {args}. kwargs: {kwargs}')

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise InternalError('Context vars list index should be an int instance')
        if len(self.__vars_list__) <= item:
            raise InternalError('Index out of range', f'Selected item: {item}')
        return self.__vars_list__[item]

    def __setitem__(self, key, value):
        raise InternalError(f'Object "Context[{key}]" is Read-Only')

    def __str__(self):
        vars_list_amount = len(self.__vars_list__)
        vars_list_elements = ', '.join([str(o) for o in self.__vars_list__])
        vars_kw_amount = len([m for m in dir(self) if not m.startswith('_')])
        vars_kw_items = ', '.join([f'{m}: {getattr(self, m, None)}' for m in dir(self) if not m.startswith('_')])
        return f'[{vars_list_elements}]({vars_list_amount}). {{{vars_kw_items}}}({vars_kw_amount})'

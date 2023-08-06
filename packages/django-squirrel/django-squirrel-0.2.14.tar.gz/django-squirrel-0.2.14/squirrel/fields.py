from squirrel.sq_types import AddressMixin, EpochDatesMixin, UIntNumbersMixin
from logging import getLogger as getLocalLogger

logger = getLocalLogger(__name__)


class FieldBase:
    raw_value = None
    field_name = ''

    def get(self):
        """Get value"""
        return self.raw_value

    @staticmethod
    def encode(value):
        return value

    def set(self, value):
        """Set value"""
        self.raw_value = self.encode(value=value)

    def __init__(self, value=None, field_name=None, required=True):
        self.field_name = field_name or self.field_name
        self.required = required
        if self.field_name is None:
            raise ValueError('Argument FieldName is required')
        if value is not None:
            self.set(value=value)

    def to_dict(self) -> dict:
        """Return {render_name: __value__}"""
        return {self.field_name: self.raw_value}

    def __str__(self):
        return '%s=%s' % (self.field_name, self.raw_value)


class AddressField(FieldBase, AddressMixin):
    """Address Field"""

    field_name = 'address'

    def encode(self, value) -> str:
        try:
            return self.checksum_address(value)
        except ValueError:
            raise ValueError('Invalid address format')


class EpochDatetimeField(FieldBase, EpochDatesMixin):
    field_name = 'datetime'

    def encode(self, value) -> int:
        return self.to_epoch(value)


class UInt256Field(FieldBase, UIntNumbersMixin):
    field_name = 'integer'

    def encode(self, value) -> int:
        return self.to_uint256(value=value)


class FourDecimalsField(FieldBase):
    field_name = 'four-decimals'

    def encode(self, value) -> int:
        return int(value * 10 ** 4)


class UInt8Field(FieldBase, UIntNumbersMixin):

    def encode(self, value) -> int:
        return self.to_uint8(value=value)


class ListField(FieldBase):
    """List Field"""

    field_name = 'list'
    raw_value = []
    __pointer__ = -1

    def __init__(self, field_name=None, list_of=FieldBase):
        super(ListField, self).__init__(required=False, field_name=field_name)
        self.__list_of__ = list_of

    def set(self, value):
        if isinstance(value, (self.__list_of__, list)):
            if isinstance(value, list):
                self.raw_value = value
            else:
                self.raw_value.append(value)
        else:
            raise TypeError('Invalid payload class. FieldList only can contains {}\'s instances. {} is not allowed'
                            ''.format(self.__list_of__.__name__, value.__class__.__name__))

    def index(self, value):
        return self.raw_value.index(value)

    def __getitem__(self, item):
        return self.raw_value[item].get()

    def append(self, value):
        self.set(value=value)

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.raw_value)

    def __next__(self):
        self.__pointer__ += 1
        if self.__pointer__ < len(self.raw_value):
            return self.raw_value[self.__pointer__].get()
        else:
            raise StopIteration

    def __str__(self):
        return '%s=[%s]' % (self.field_name, ', '.join([str(x.get()) for x in self.raw_value]))

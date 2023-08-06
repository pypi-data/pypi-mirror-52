from logging import getLogger as getLocalLogger
from squirrel.exceptions import BadRequest
from pika import BasicProperties
from arrow import now
import json

logger = getLocalLogger(__name__)


class Header:
    """Key/Value Header representation"""
    __key_name__ = ''
    __value__ = ''

    def __init__(self, key, value):
        self.__key_name__ = key
        self.__value__ = value

    def encode(self, value):
        """Encode HEADER value"""
        return value

    def decode(self, value):
        """Decode HEADER value"""
        return value

    @property
    def name(self):
        return self.__key_name__

    @property
    def value(self):
        return self.decode(self.__value__)

    @value.setter
    def value(self, value):
        self.__value__ = self.encode(value=value)

    @property
    def to_dict(self):
        return {self.__key_name__: self.decode(value=self.__value__)}

    def __str__(self):
        return f'{self.__key_name__}={self.__value__}'


class HeaderManager:
    """Headers manager"""
    __headers__: [Header] = []

    def __init__(self, **headers):
        for key, value in headers.items():
            self.add(key_name=key, value=value)

    def search(self, key_name) -> tuple:
        """Exists header?"""
        try:
            h_pos = [header.name for header in self.__headers__].index(key_name)
            return True, h_pos
        except ValueError:
            return False, None

    def export_as_properties(self, **extra_keys) -> BasicProperties:
        return BasicProperties(headers=self.__call__(raw=False), **extra_keys)

    def add(self, key_name, value, index=None):
        try:
            json.dumps({key_name: value})
        except json.decoder.JSONDecodeError:
            raise ValueError('Invalid header')
        if isinstance(index, int) and all([index > -1, index < len(self.__headers__)]):
            self.__headers__[index].value = value
        else:
            is_created, index = self.search(key_name=key_name)
            if is_created:
                self.__headers__[index].value = value
            else:
                self.__headers__.append(Header(key=key_name, value=value))

    def update(self, key_name, value, header_must_exists=True):
        """add wrapper"""
        created, index = self.search(key_name=key_name)
        if not created and header_must_exists:
            raise KeyError(f'Header {key_name} does not search')
        self.add(key_name=key_name, value=value, index=index)

    def __call__(self, raw=False) -> list or dict:
        """Dump headers"""
        if raw:
            return self.__headers__
        return {h.name: h.value for h in self.__headers__}

    def __getitem__(self, header):
        created, index = self.search(key_name=header)
        if not created:
            raise IndexError(f'Header "{header}" does not search')
        return self.__headers__[index].value

    def __setitem__(self, header, value):
        self.update(key_name=header, value=value)

    def __str__(self):
        return f'{json.dumps(self.__call__(raw=False), indent=4)}'


class Request:
    """Request Base"""
    headers: HeaderManager = None

    PENDING = 'pending'
    SOLVED = 'solved'
    ERROR_BAD_REQUEST = 'bad-request'
    ERROR_NOT_FOUND = 'not-found'
    ERROR_FAILED = 'failed'

    ALLOWED_STATUS = \
        {
            PENDING: 'Pending request',
            SOLVED: 'Resolved request',
            ERROR_BAD_REQUEST: 'Error: Bad Request',
            ERROR_NOT_FOUND: 'Error: Method Not Found',
            ERROR_FAILED: 'Error: Task failed'
        }

    received_at = None
    solved_at = None
    data = None
    raw_data = None
    processed_data = None
    url = None
    _params = None
    _id = None
    _method = None
    json_rpc = '2.0'  # remove hard-code
    _status = PENDING

    def initialize(self, raw_data):
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode()
        self.raw_data = raw_data
        self.received_at = now().format('YYYY-MM-DD HH:mm:ss')
        try:
            self.processed_data = json.loads(self.raw_data)
        except Exception as e:
            raise BadRequest('No json serializable request')

    def __init__(self, headers=None, **data):
        headers = headers or {}
        # Import headers
        self.headers = HeaderManager(**headers)
        # import data
        self.initialize(**data)

    def __property_loader__(self, property_name):
        if getattr(self, f'_{property_name}') is not None:
            return True
        if not hasattr(self, f'_{property_name}'):
            raise BadRequest(f'{property_name} is not supported')
        processed_data = self.processed_data
        if not isinstance(processed_data, dict):
            raise BadRequest('Loaded data fails')
        if processed_data is None:
            raise BadRequest('Empty request')
        setattr(self, f'_{property_name}', self.processed_data.get(property_name))

    @property
    def method(self):
        self.__property_loader__(property_name='method')
        return self._method

    @property
    def id(self):
        self.__property_loader__(property_name='id')
        return self._id

    @property
    def params(self):
        self.__property_loader__(property_name='params')
        return self._params

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.ALLOWED_STATUS.keys():
            raise BadRequest(f'{value} is not supported')
        self._status = value

    def __str__(self):
        return f'ID#{self.id} ' \
            f'Received at: {self.received_at}. ' \
            f'Status: {self.status.upper()}. ' \
            f'Method: {self.method.upper()}'

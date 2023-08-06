from logging import getLogger as getLocalLogger
from squirrel.exceptions import BadRequest
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

    @property
    def name(self):
        return self.__key_name__

    @property
    def value(self):
        return self.__value__

    @property
    def to_dict(self):
        return {self.__key_name__: self.__value__}

    def __str__(self):
        return f'{self.__key_name__}={self.__value__}'


class Request:
    """Request Base"""
    __headers__ = []

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

    def __init__(self, **data):
        self.initialize(**data)

    @property
    def headers(self):
        return self.__headers__

    def add_header(self, key_name, value):
        try:
            json.dumps({key_name: value})
        except json.decoder.JSONDecodeError:
            raise ValueError('Invalid header')
        self.__headers__.append(Header(key=key_name, value=value))

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
            raise BadRequest('{} is not supported.'.format(value))
        self._status = value

    def __str__(self):
        return f'ID#{self.id} ' \
            f'Received at: {self.received_at}. ' \
            f'Status: {self.status.upper()}. ' \
            f'Method: {self.method.upper()}'

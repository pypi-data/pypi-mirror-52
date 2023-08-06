from squirrel.exceptions import BadRequest, NotFocusedView, MiddlewareNotFound
from logging import getLogger as getLocalLogger
from squirrel.responses import Response
from squirrel.requests import Request
from importlib import import_module
from django.conf import settings

logger = getLocalLogger(__name__)


class Middleware:
    """Middleware Base"""
    _context = None
    request = None
    response = None

    @property
    def name(self):
        return f'{self.__class__.__name__}'

    def __init__(self, request, context=None):
        if isinstance(request, Request):
            self.request = request
        elif isinstance(request, Response):
            self.response = request
        self._context = context or self._context
        self.load()

    def pre_process(self, request, context) -> (Request, Response):
        logger.warning(f'Middleware pre-process: {self}')
        logger.warning(f'{"Incoming" if isinstance(request, Response) else "Outgoing"} request: {request}')
        logger.warning(f'Data: {context or "no-data"}')
        return request

    def load(self):
        """Load middleware"""
        logger.debug(f'Loading middleware {self} ...')
        self.request = self.pre_process(request=self.request, context=self._context)
        logger.info(f'Middleware {self} successfully loaded.')

    def process_incoming_flow(self) -> Request:
        return self.request

    def process_outgoing_flow(self) -> Response:
        return self.response

    def process(self) -> (Request, Response):
        if isinstance(self.request, Request):
            return self.process_incoming_flow()
        if isinstance(self.response, Response):
            return self.process_outgoing_flow()
        raise BadRequest('Invalid Request/Response')

    def __str__(self):
        return '%s' % self.name


class CommonMiddleware(Middleware):
    """Common middleware"""


class SecurityValidationCheck(Middleware):
    """Security Middleware"""


class FocusOnMiddleware(Middleware):
    """Single view middleware"""
    focus_url = '__unfocused__'

    def process_incoming_flow(self) -> Request:
        """Block request for distinct than `self.focus_url`"""
        _focus_url = getattr(settings, 'FOCUS_URL', None) or self.focus_url
        if not isinstance(self.focus_url, str):
            raise ValueError(f'Unsupported focus_url class. '
                             f'"focus_url" value: "{self.focus_url}". '
                             f'FOCUS_URL should be something more like "/path-to/view" ;)')
        focus_is_enable = not _focus_url == '__unfocused__'
        if not self.focus_url == self.request.url and focus_is_enable:
            raise NotFocusedView
        return self.request


default_middleware_layers = \
    [
        'squirrel.middleware.CommonMiddleware',
        'squirrel.middleware.FocusOnMiddleware',
        'squirrel.middleware.SecurityValidationCheck'
    ]


class MiddlewareManager:
    """Middleware Manager"""
    initialized: bool = False
    middleware_classes = getattr(settings, 'SQUIRREL_MIDDLEWARE', []) + default_middleware_layers

    def initialize(self):
        if not isinstance(self.middleware_classes, list):
            raise TypeError('Unsupported middleware classes list')
        _mwc = []
        for middleware_path in self.middleware_classes:
            if not isinstance(middleware_path, str):
                raise TypeError('unsupported middleware path class. STR instance expected')
            if len(middleware_path) == 0:
                raise ValueError('middleware_path EMPTY')
            _mwc.append(self.import_middleware_from_path(middleware_path=middleware_path))
        self.middleware_classes = _mwc
        self.initialized = True

    @staticmethod
    def import_middleware_from_path(middleware_path: str) -> Middleware:
        """Import Middleware classes"""
        try:
            app_name, module_name, class_name = middleware_path.split('.')
            _module = import_module(f'{app_name}.{module_name}')
            if not hasattr(_module, class_name):
                raise AttributeError(f'Middleware module not has attribute {class_name}')
            _middleware_class = getattr(_module, class_name)
            if not isinstance(_middleware_class, Middleware):
                raise TypeError('Unsupported middleware class')
            return _middleware_class
        except ModuleNotFoundError:
            msg = f'Middleware path: "{middleware_path}"'
            logger.exception(f'ValueError: {msg}')
            raise MiddlewareNotFound(msg)
        except ValueError as ve:
            msg = f'Malformed middleware path. {ve}'
            logger.exception(f'ValueError: {msg}')
            raise ValueError(msg)
        except Exception as e:
            logger.exception(f'{e.__class__.__name__}: "{e}"')

    def middleware(self, request) -> (Request, Response):
        """Process routes's middleware layer"""
        if not self.initialized:
            self.initialize()
        if isinstance(request, (Request, Response)):
            # Incoming Flow
            logger.debug(f'Rendering incoming/outgoing flow. Request/Response: {request}.')
            for middleware_class in self.middleware_classes:
                middleware = middleware_class(request=request, context=request.params)
                request = middleware.process()
            return request


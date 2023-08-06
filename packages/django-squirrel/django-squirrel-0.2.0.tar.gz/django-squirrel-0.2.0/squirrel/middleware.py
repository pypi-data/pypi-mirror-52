from squirrel.exceptions import BadRequest
from squirrel.responses import Response
from squirrel.requests import Request
import logging


logger = logging.getLogger(__name__)


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


class MiddlewareManager:
    """Middleware Manager"""
    middleware_classes = [CommonMiddleware, SecurityValidationCheck]

    def middleware(self, request) -> (Request, Response):
        """Process routes's middleware layer"""
        if isinstance(request, (Request, Response)):
            # Incoming Flow
            logger.debug(f'Rendering incoming/outgoing flow. Request/Response: {request}.')
            for middleware_class in self.middleware_classes:
                middleware = middleware_class(request=request, context=request.params)
                request = middleware.process()
            return request

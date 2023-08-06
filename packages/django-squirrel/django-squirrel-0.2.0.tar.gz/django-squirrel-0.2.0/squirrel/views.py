from squirrel.exceptions import BadRequest
from squirrel.responses import Response
from squirrel.contexts import Context
from squirrel.requests import Request
from arrow import now
import logging


# logger instance
logger = logging.getLogger(__name__)


class View:
    """JSON-RPC base view"""
    _request = None
    _context = {}
    logger = None
    outgoing_method = None

    def __init__(self, request, context=None):
        if not isinstance(request, Request):
            raise TypeError('{} request is not supported'.format(request.__class__.__name__))
        if not isinstance(context, Context):
            raise TypeError('{} context is not supported'.format(context.__class__.__name__))
        self._request = request
        self._context = context or {}

    def render(self) -> Response:
        if not isinstance(self._context, Context):
            raise BadRequest('Invalid params')
        logger.info(f'Context: {self._context}')
        logger.info(f'Request: {self._request}')
        response = self.get(request=self._request, context=self._context)
        response.id = self._request.id
        response.url = response.url or self._request.url
        response.method = self.outgoing_method or self._request.method
        response.received_at = self._request.received_at
        response.solved_at = now().format('YYYY-MM-DD HH:mm:ss')
        return response

    def get(self, request, context) -> Response:
        logger.warning(f'{self} default get method')
        logger.warning(f'Context: {context}')
        return Response(params=request.params, send_payload=False)

    def __str__(self):
        return '%s' % self.__class__.__name__


class PingView(View):
    """Ping view"""
    outgoing_method = 'pong'

    def get(self, request, context) -> Response:
        logger.info(f'Ping! {request}')
        return Response(params=['pong'])


class PongView(View):
    """Pong view"""

    outgoing_method = None

    def get(self, request, context) -> Response:
        logger.info(f'Pong! {request}')
        return Response(params=['pong'], send_payload=False)

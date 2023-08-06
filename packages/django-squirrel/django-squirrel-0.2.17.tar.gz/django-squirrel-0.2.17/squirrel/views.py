from logging import getLogger as getLocalLogger
from squirrel.exceptions import BadRequest
from squirrel.responses import Response
from squirrel.contexts import Context
from squirrel.requests import Request
from django.conf import settings
from arrow import now

logger = getLocalLogger(__name__)


class View:
    """JSON-RPC base view"""
    _request = None
    _context = {}
    outgoing_method = None

    def __init__(self, request, context=None):
        if not isinstance(request, Request):
            raise TypeError(f'{request.__class__.__name__} request is not supported')
        if not isinstance(context, Context):
            raise TypeError(f'{context.__class__.__name__} context is not supported')
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


class InfoView(View):
    """Info view"""

    outgoing_method = 'worker_info'

    @staticmethod
    def get_squirrel_data() -> dict:
        w_info = {
            'port': settings.RABBIT_MQ_PORT,
            'hostname': settings.RABBIT_MQ_HOSTNAME,
            'username': settings.RABBIT_MQ_USERNAME,
            'virtual-host': settings.RABBIT_MQ_VIRTUAL_HOST,
            'incoming-queue': settings.INCOMING_QUEUE,
            'outgoing-queue': settings.OUTGOING_QUEUE,
        }
        demo_mode = getattr(settings, 'SQUIRREL_DEMO', False)
        if demo_mode:
            __password__ = settings.RABBIT_MQ_PASSWORKD
        else:
            __password__ = 'Passwords only are showed on DEMO mode ON'
        w_info.update({'password': __password__})
        return w_info

    def get(self, request, context) -> Response:
        logger.info(f'Worker info. {request}')
        return Response(params=self.get_squirrel_data(), send_payload=False)

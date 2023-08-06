from logging import getLogger as getLocalLogger
from squirrel.requests import Request
from arrow import now
import json

logger = getLocalLogger(__name__)


class Response(Request):
    """Response base"""
    _payload = None
    queue = None
    exchange = ''
    routing_key = ''
    send_payload = True

    params = None
    method = None
    id = None

    def initialize(self, params=None, status=Request.SOLVED, send_payload=True, routing_key=''):
        """Initialize response"""
        self.routing_key = routing_key
        self.send_payload = send_payload
        self.status = status
        self.params = [params] if not isinstance(params, (list, dict)) else params
        self.solved_at = now().format('YYYY-MM-DD HH:mm:ss')

    def prepare_payload(self):
        """Prepare response payload"""
        payload = json.dumps({
            'method': self.method,
            'params': self.params,
            'id': self.id,
            'json-rpc': self.json_rpc,
        })
        return payload.encode()

    @property
    def payload(self):
        """Get response payload"""
        return self.prepare_payload()

    def __str__(self):
        return f'{super().__str__()}. Solved at:{self.solved_at}'


class EmptyResponse(Response):
    """Empty response"""

    send_payload = False
    id = 0
    method = 'empty-method'
    params = []


class StopPropagation(EmptyResponse):
    """Stop request propagation"""
    def __init__(self):
        super().__init__(send_payload=False)
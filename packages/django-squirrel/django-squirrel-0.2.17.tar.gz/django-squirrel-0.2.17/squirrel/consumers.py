from squirrel.exceptions import NotFound, URLNotFound, MiddlewareNotFound, MethodNotFound, BadRequest, InternalError
from django.core.exceptions import ObjectDoesNotExist
from squirrel.connections import RabbitConnection
from squirrel.utils import JSONRPCEncoderDecoder
from logging import getLogger as getLocalLogger
from squirrel.helpers import ForkProcess
from squirrel.firewalls import Firewall
from squirrel.requests import Request
from django.conf import settings
from squirrel.urls import router

logger = getLocalLogger(__name__)


class Consumer(RabbitConnection, ForkProcess, Firewall, JSONRPCEncoderDecoder):
    """Consumer Mixin"""

    def bind(self):
        logger.debug(f'Binding: {self}')
        logger.debug(f'Opening connection ...')
        self.init_fork(nb_workers=(getattr(settings, 'SQUIRREL_WORKER_THREADS', 1)))
        self.open()
        logger.debug(f'Connection {self} successfully opened')
        try:
            logger.info(f'{self} now is listening ...')
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.disconnect()
            # stop all threads
            self.terminate()
            raise KeyboardInterrupt

    def open(self):
        super(Consumer, self).open()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message)

    def create_request(self, raw_data, headers=None, routing_key=None) -> Request:
        request = Request(raw_data=raw_data, headers=headers or {})
        request.url = f'/{routing_key or self.queue_name}/{request.method}'
        return request

    def on_message_callback(self, payload):
        routing_key = payload.get('routing_key')
        body = payload.get('body')
        headers = payload.get('headers', {})
        request = self.create_request(raw_data=body, headers=headers, routing_key=routing_key)
        router.submit_request(request=request)

    def on_success_callback(self, payload, result_data): ...

    def on_error_callback(self, payload, exception_raised):
        """OnError Callback"""
        if isinstance(exception_raised, (NotFound, MethodNotFound, URLNotFound, ObjectDoesNotExist)):
            # 404's Errors
            logger.debug(f'404.Not found error. {exception_raised}')
        if isinstance(exception_raised, BadRequest):
            # 403's Errors
            logger.warning(f'403. Bad request error. {exception_raised}')
        if isinstance(exception_raised, (MiddlewareNotFound, InternalError, Exception)):
            # 500's Errors
            # TODO:
            #  + Define requeue condition
            #  + Re-submit message on retry needed cases
            logger.critical(f'500. Internal error. {exception_raised}')

    def on_message(self, ch, method, properties, body):
        """On message callback"""
        _new_request = {
            'routing_key': method.routing_key,
            'body': body,
            'headers': properties.headers,
        }
        # Submit new request to processors pool
        try:
            self.firewall(**_new_request)
            self.resolve_task(payload=_new_request)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f'{e}')
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

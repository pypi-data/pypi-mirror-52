from squirrel.connections import RabbitConnection, RabbitConnectionParameters, RabbitCredentials
from squirrel.middleware import MiddlewareManager
from squirrel.utils import JSONRPCEncoder
from django.conf import settings
import logging


# logger instance
logger = logging.getLogger(__name__)


class PublisherMixin(RabbitConnection, JSONRPCEncoder, MiddlewareManager):
    """Publisher Mixin"""
    queue_name = settings.OUTGOING_QUEUE

    def _configure(self):
        """Configure publisher"""
        self.queue_name = settings.OUTGOING_QUEUE
        self.connection_params = RabbitConnectionParameters(virtual_host=settings.RABBIT_MQ_VIRTUAL_HOST,
                                                            port=settings.RABBIT_MQ_PORT,
                                                            host=settings.RABBIT_MQ_HOSTNAME,
                                                            credentials=RabbitCredentials(
                                                                username=settings.RABBIT_MQ_USERNAME,
                                                                password=settings.RABBIT_MQ_PASSWORD))

    def publish(self, response):
        """Publish message `response`"""
        logger.info('Publishing ...')
        self._configure()
        self.open()
        logger.debug('Connection successful opened')
        try:
            response = self.middleware(response)
            logger.debug(response.routing_key)
            logger.debug(response.payload)
            self.channel.basic_publish(exchange='',
                                       routing_key=response.routing_key,
                                       body=response.payload,
                                       properties=response.export_as_properties(content_type='application/json'))
            logger.info('Message successful published')
        except Exception as e:
            logger.error(e)
        self.disconnect()
        logger.debug('Disconnected')


def get_logger() -> PublisherMixin:
    """Returns Publisher instance"""
    return PublisherMixin()

from logging import getLogger as getLocalLogger
from pika import \
    PlainCredentials as PikaPlainCredentials, \
    ConnectionParameters as PikaConnectionParameters, \
    BlockingConnection as PikaBlockingConnection


logger = getLocalLogger(__name__)


class Credentials:
    user = ''
    password = ''

    def __init__(self, username=None, password=None):
        self.user = username or self.user
        self.password = password or self.password

    def get(self):
        """Resolve user password"""
        return f'{self.user}:{self.password}'


class RabbitCredentials(Credentials):
    """Rabbit Credentials"""

    def get(self):
        return PikaPlainCredentials(username=self.user, password=self.password)


class ConnectionParameters:
    """Connection Parameters"""
    host: str = ''
    port: int = 0

    def __init__(self, host=None, port=None):
        self.port = port or self.port
        self.host = host or self.host

    def get(self):
        return f'{self.host}:{self.port}'


class RabbitConnectionParameters(ConnectionParameters):
    """Rabbit Connections Parameters"""

    virtual_host: str = ''
    credentials = None

    def __init__(self, host, port, credentials=None, virtual_host=None):
        super().__init__(host=host, port=port)
        self.credentials = credentials or self.credentials
        self.virtual_host = virtual_host or self.virtual_host

    def get(self):
        return PikaConnectionParameters(host=self.host, port=self.port, virtual_host=self.virtual_host,
                                        credentials=self.credentials.get())


class Connection:
    """Connection"""

    name: str = 'Connection'
    connection = None
    channel = None

    def __init__(self, name=None):
        self.name = name or self.name

    def write(self): ...

    def bind(self): ...

    def on_message(self, *args, **kwargs): ...

    def open(self): ...

    def disconnect(self): ...

    def __str__(self):
        return '%s' % self.name


class RabbitConnection(Connection):
    """Rabbit Connection"""
    name = 'rabbit-mq-connection'
    connection_params = None
    queue_name: str = ''
    default_exchange: str = ''
    default_routing_key: str = ''
    logger = None

    def __init__(self, connection_params=None, queue=None, exchange=None, routing_key=None):
        super().__init__(name='RabbitMQConnection')
        self.connection_params = connection_params or self.connection_params
        self.queue_name = queue or self.queue_name
        self.default_exchange = exchange or self.default_exchange
        self.default_routing_key = routing_key or self.default_routing_key

    def open(self):
        """Open connection"""
        logger.debug('Connecting ...')
        self.connection = PikaBlockingConnection(parameters=self.connection_params.get())
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        logger.debug('Connected')

    def disconnect(self):
        """Close connection"""
        logger.debug('Closing connection ...')
        self.connection.close()
        logger.debug('Connection closed.')

    def __str__(self):
        return 'Consumer: %s. Queue: %s' % (super().__str__(), self.queue_name)


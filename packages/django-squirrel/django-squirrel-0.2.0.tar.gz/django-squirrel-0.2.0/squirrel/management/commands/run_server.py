"""
Run squirrel server
"""
from squirrel.events import on_close_tasks, on_init_tasks, on_abnormal_close_tasks
from squirrel.connections import RabbitConnectionParameters, RabbitCredential
from django.core.management.base import BaseCommand
from squirrel.consumers import Consumer
from django.conf import settings
from arrow import now
import logging
import os

# Logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# RPC Server help
START_JSON_RPC_SERVER_HELP = """
Run JSON-RPC Server
"""

JSON_RPC_RUNSERVER_SPLASH = """
---------------------------------------------------------------------
      _________            .__                      .__   
     /   _____/ ________ __|__|_____________   ____ |  |
     \_____  \ / ____/  |  \  \_  __ \_  __ \_/ __ \|  |  
     /        < <_|  |  |  /  ||  | \/|  | \/\  ___/|  |__
    /_______  /\__   |____/|__||__|   |__|    \___  >____/
            \/    |__|                            \/      
            
    Version: 0.2.0.katana.13092019
    Started at: {now_datetime}    
    Connected to:     
    - rabbit_mq://{username}:*****@{hostname}:{port}{virtual_host}
    
    Queues:
    - Incoming: {incoming_queue}
    - Outgoing: {outgoing_queue}

---------------------------------------------------------------------
"""

HERE = os.path.dirname(os.path.abspath(__name__))

DEFAULT_PORT = 5672
DEFAULT_HOSTNAME = 'localhost'
DEFAULT_USERNAME = 'guest'
DEFAULT_PASSWORD = 'guest'
DEFAULT_VH = '/'

DEFAULT_INCOMING_QUEUE = 'blockchain'
DEFAULT_OUTGOING_QUEUE = 'api'


class ConnectionConfig:
    # Rabbit connection
    hostname = getattr(settings, 'RABBIT_MQ_HOSTNAME', DEFAULT_HOSTNAME)
    username = getattr(settings, 'RABBIT_MQ_USERNAME', DEFAULT_USERNAME)
    password = getattr(settings, 'RABBIT_MQ_PASSWORD', DEFAULT_PASSWORD)
    port = getattr(settings, 'RABBIT_MQ_PORT', DEFAULT_PORT)
    virtual_host = getattr(settings, 'RABBIT_MQ_VIRTUAL_HOST', DEFAULT_VH)
    # Connections
    incoming_queue = getattr(settings, 'INCOMING_QUEUE', DEFAULT_INCOMING_QUEUE)
    outgoing_queue = getattr(settings, 'OUTGOING_QUEUE', DEFAULT_OUTGOING_QUEUE)

    def update(self, hostname=None, username=None, password=None,
               port=None, virtual_host=None, incoming_queue=None, outgoing_queue=None):
        """Update django.conf.settings VARs"""
        settings.RABBIT_MQ_HOSTNAME = hostname or self.hostname
        settings.RABBIT_MQ_USERNAME = username or self.username
        settings.RABBIT_MQ_PASSWORD = password or self.password
        settings.RABBIT_MQ_PORT = port or self.port
        settings.RABBIT_MQ_VIRTUAL_HOST = virtual_host or self.virtual_host
        settings.INCOMING_QUEUE = incoming_queue or self.incoming_queue
        settings.OUTGOING_QUEUE = outgoing_queue or self.outgoing_queue

    def __str__(self):
        return f'Hostname: {self.hostname}. Username: {self.username}. Password: *****. '


# Default config
default_config = ConnectionConfig()


class Command(BaseCommand):
    """Run JSON-RPC server"""
    help = START_JSON_RPC_SERVER_HELP

    def add_arguments(self, parser):
        # Rabbit connection:
        parser.add_argument('--port', type=str, help='RabbitMQ Custom Port', default=default_config.port)
        parser.add_argument('--hostname', type=str, help='RabbitMQ Custom Host', default=default_config.hostname)
        parser.add_argument('--username', type=str, help='RabbitMQ Custom username', default=default_config.username)
        parser.add_argument('--password', type=str, help='RabbitMQ Custom password', default=default_config.password)
        parser.add_argument('--virtual-host', type=str, help='RabbitMQ Custom virtual-host', default=default_config.virtual_host)
        # Incoming connections:
        parser.add_argument('--incoming-queue', type=str, help='RabbitMQ Custom Incoming queue', default=default_config.incoming_queue)
        # Outgoing connections:
        parser.add_argument('--outgoing-queue', type=str, help='RabbitMQ Custom Outgoing queue', default=default_config.outgoing_queue)

    def handle(self, *args, **options):
        incoming_queue = options.get('incoming_queue')
        outgoing_queue = options.get('outgoing_queue')
        hostname = options.get('hostname')
        port = options.get('port')
        username = options.get('username')
        password = options.get('password')
        virtual_host = options.get('virtual_host')
        print(flush=True)
        print(JSON_RPC_RUNSERVER_SPLASH.format(
            incoming_queue=incoming_queue,
            outgoing_queue=outgoing_queue,
            hostname=hostname,
            port=port,
            username=username,
            virtual_host=virtual_host,
            now_datetime=now().format('YYYY-MM-DD HH:mm:ss')
        ), flush=True)
        # update config:
        default_config.update(hostname=hostname, port=port,
                              username=username, password=password,
                              virtual_host=virtual_host, incoming_queue=incoming_queue,
                              outgoing_queue=outgoing_queue)
        print(flush=True)
        # Process OnInit hooks
        on_init_tasks.raise_event()
        try:
            consumer = Consumer(
                exchange='',
                queue=incoming_queue,
                connection_params=RabbitConnectionParameters(port=port,
                                                             host=hostname,
                                                             virtual_host=virtual_host,
                                                             credentials=RabbitCredential(username=username,
                                                                                          password=password)))
            consumer.bind()
        except KeyboardInterrupt:
            on_close_tasks.raise_event()
            logger.info('Normal finalization')
        except Exception as e:
            on_abnormal_close_tasks.raise_event()
            logger.critical(f'Abnormal finalization. {e}')

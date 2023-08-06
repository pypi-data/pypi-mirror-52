"""
Run squirrel server
"""
from squirrel.events import on_close_tasks, on_init_tasks, on_abnormal_close_tasks
from squirrel.connections import RabbitConnectionParameters, RabbitCredentials
from django.core.management.base import BaseCommand
from squirrel.consumers import Consumer
from django.conf import settings
from arrow import now
import logging


# Logger instance
logger = logging.getLogger(__name__)

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

    Version: {version}.{codename}.{release_date}
    Started at: {now_datetime}    
    Connected to:     
    - rabbit_mq://{username}:*****@{hostname}:{port}{virtual_host}
    
    Queues:
    - Incoming: {incoming_queue}
    - Outgoing: {outgoing_queue}

---------------------------------------------------------------------
"""


class Command(BaseCommand):
    """Run JSON-RPC server"""
    help = START_JSON_RPC_SERVER_HELP

    def add_arguments(self, parser):
        # Rabbit connection:
        parser.add_argument('--port', type=str, help='RabbitMQ Custom Port', default=getattr(settings, 'RABBIT_MQ_PORT'))
        parser.add_argument('--hostname', type=str, help='RabbitMQ Custom Host', default=getattr(settings, 'RABBIT_MQ_HOSTNAME'))
        parser.add_argument('--username', type=str, help='RabbitMQ Custom username', default=getattr(settings, 'RABBIT_MQ_USERNAME'))
        parser.add_argument('--password', type=str, help='RabbitMQ Custom password', default=getattr(settings, 'RABBIT_MQ_PASSWORD'))
        parser.add_argument('--virtual-host', type=str, help='RabbitMQ Custom virtual-host', default=getattr(settings, 'RABBIT_MQ_VIRTUAL_HOST'))
        # Incoming connections:
        parser.add_argument('--incoming-queue', type=str, help='RabbitMQ Custom Incoming queue', default=getattr(settings, 'INCOMING_QUEUE'))
        # Outgoing connections:
        parser.add_argument('--outgoing-queue', type=str, help='RabbitMQ Custom Outgoing queue', default=getattr(settings, 'OUTGOING_QUEUE'))

    def handle(self, *args, **options):
        # Update django settings.vars
        virtual_host = options.get('virtual_host')
        incoming_queue = options.get('incoming_queue')
        outgoing_queue = options.get('outgoing_queue')
        hostname = options.get('hostname')
        username = options.get('username')
        password = options.get('password')
        port = options.get('port')
        setattr(settings, 'RABBIT_MQ_PORT', port)
        setattr(settings, 'RABBIT_MQ_HOSTNAME', hostname)
        setattr(settings, 'RABBIT_MQ_USERNAME', username)
        setattr(settings, 'RABBIT_MQ_PASSWORD', password)
        setattr(settings, 'INCOMING_QUEUE', incoming_queue)
        setattr(settings, 'OUTGOING_QUEUE', outgoing_queue)
        setattr(settings, 'RABBIT_MQ_VIRTUAL_HOST',  virtual_host)
        print(flush=True)
        print(JSON_RPC_RUNSERVER_SPLASH.format(

            incoming_queue=incoming_queue,
            outgoing_queue=outgoing_queue,
            hostname=hostname,
            port=port,
            username=username,
            virtual_host=virtual_host,
            now_datetime=now().format('YYYY-MM-DD HH:mm:ss'),
            release_date=getattr(settings, 'SQUIRREL_RELEASE_DATE', '----'),
            version=getattr(settings, 'SQUIRREL_VERSION', '0.0.0'),
            codename=getattr(settings, 'SQUIRREL_CODENAME', '--------'),
        ), flush=True)
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
                                                             credentials=RabbitCredentials(username=username,
                                                                                           password=password)))
            consumer.bind()
        except KeyboardInterrupt:
            on_close_tasks.raise_event()
            logger.info('Normal finalization')
        except Exception as e:
            on_abnormal_close_tasks.raise_event()
            logger.critical(f'Abnormal finalization. {e}')

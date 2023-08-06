"""
Run squirrel server
"""
from squirrel.events import on_close_tasks, on_init_tasks, on_abnormal_close_tasks
from squirrel.connections import RabbitConnectionParameters, RabbitCredentials
from django.core.management.base import BaseCommand
from squirrel.helpers import SquirrelCommandHelper
from squirrel.consumers import Consumer
import logging

# Logger instance
logger = logging.getLogger(__name__)


class Command(BaseCommand, SquirrelCommandHelper):
    """Run JSON-RPC server"""

    def add_arguments(self, parser):
        self.default_arguments(parser=parser)
        self.extra_arguments(parser=parser)

    def handle(self, *args, **options):
        """Handle command RUN_SERVER"""
        self.st_log_level(int(options.get('verbosity')))
        self.update_env_vars(**options)
        self.print_splash()
        # Process OnInit hooks
        on_init_tasks.raise_event()
        try:
            _rc = RabbitCredentials(username=options.get('username'), password=options.get('password'))
            _rcp = RabbitConnectionParameters(port=options.get('port'), host=options.get('hostname'),
                                              virtual_host=options.get('virtual_host'),
                                              credentials=_rc)
            consumer = Consumer(exchange='',
                                queue=options.get('incoming_queue'),
                                connection_params=_rcp)
            consumer.bind()
        except KeyboardInterrupt:
            on_close_tasks.raise_event()
            logger.info('Normal finalization')
        except Exception as e:
            on_abnormal_close_tasks.raise_event()
            logger.critical(f'Abnormal finalization. {e}')

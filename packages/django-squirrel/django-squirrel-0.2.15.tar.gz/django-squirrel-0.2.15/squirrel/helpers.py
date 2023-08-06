"""
Squirrel Helpers
"""
from logging import getLogger as getLocalLogger, DEBUG, INFO, WARNING, ERROR
from django.conf import settings
import multiprocessing as mp
from arrow import now
from squirrel.settings import local_vars

logger = getLocalLogger(__name__)


class SquirrelCommandHelper:
    """Squirrel command helper"""
    # RPC Server help
    START_JSON_RPC_SERVER_HELP = """
    Run JSON-RPC Server
    """
    help = START_JSON_RPC_SERVER_HELP
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
    @staticmethod
    def update_default_vars(**inputs):
        for var_name, default_value in local_vars.items():
            custom_value = inputs.get(var_name)
            setattr(settings, var_name, default_value if custom_value is None else custom_value)

    @staticmethod
    def st_log_level(log_level=None):
        log_levels = [ERROR, WARNING, INFO, DEBUG]
        if not isinstance(log_level, int) or log_level > len(log_levels):
            log_level = log_levels.index(DEBUG)
        root_logger = getLocalLogger('')
        root_logger.setLevel(log_level)

    def update_extra_vars(self, **inputs): ...

    def update_env_vars(self, **inputs):
        self.update_default_vars(**inputs)
        self.update_extra_vars(**inputs)

    def print_splash(self):
        """Print worker splash"""
        print(flush=True)
        print(self.JSON_RPC_RUNSERVER_SPLASH.format(
            incoming_queue=getattr(settings, 'INCOMING_QUEUE'),
            outgoing_queue=getattr(settings, 'OUTGOING_QUEUE'),
            hostname=getattr(settings, 'RABBIT_MQ_HOSTNAME'),
            port=getattr(settings, 'RABBIT_MQ_PORT'),
            username=getattr(settings, 'RABBIT_MQ_USERNAME'),
            virtual_host=getattr(settings, 'RABBIT_MQ_VIRTUAL_HOST'),
            now_datetime=now().format('YYYY-MM-DD HH:mm:ss'),
            release_date=getattr(settings, 'SQUIRREL_RELEASE_DATE', '----'),
            version=getattr(settings, 'SQUIRREL_VERSION', '0.0.0'),
            codename=getattr(settings, 'SQUIRREL_CODENAME', '--------'),
        ), flush=True)
        print(flush=True)

    @staticmethod
    def default_arguments(parser):
        parser.add_argument('--port',
                            type=str,
                            help='RabbitMQ Custom Port',
                            default=getattr(settings, 'RABBIT_MQ_PORT'))
        parser.add_argument('--hostname',
                            type=str,
                            help='RabbitMQ Custom Host',
                            default=getattr(settings, 'RABBIT_MQ_HOSTNAME'))
        parser.add_argument('--username',
                            type=str,
                            help='RabbitMQ Custom username',
                            default=getattr(settings, 'RABBIT_MQ_USERNAME'))
        parser.add_argument('--password',
                            type=str,
                            help='RabbitMQ Custom password',
                            default=getattr(settings, 'RABBIT_MQ_PASSWORD'))
        parser.add_argument('--virtual-host',
                            type=str,
                            help='RabbitMQ Custom virtual-host',
                            default=getattr(settings, 'RABBIT_MQ_VIRTUAL_HOST'))
        # Incoming connections:
        parser.add_argument('--incoming-queue',
                            type=str,
                            help='RabbitMQ Custom Incoming queue',
                            default=getattr(settings, 'INCOMING_QUEUE'))
        # Outgoing connections:
        parser.add_argument('--outgoing-queue',
                            type=str,
                            help='RabbitMQ Custom Outgoing queue',
                            default=getattr(settings, 'OUTGOING_QUEUE'))

    def extra_arguments(self, parser): ...  # Todo


class ForkProcess:
    queue = None
    logger = None
    nb_workers = 4
    lock = None
    stop_signal = None
    processes = []

    def init_fork(self, nb_workers=None):
        logger.info('Starting process queue ...')
        self.queue = mp.JoinableQueue()
        for idx in range(nb_workers or self.nb_workers):
            self.processes.append(
                mp.context.Process(target=self.process_task, args=(idx, ))
            )
        for p in self.processes:
            p.start()
        logger.info(f'Process queue started. Threads running {len(self.processes)}.')

    def resolve_task(self, payload):
        self.queue.put(payload)

    def on_success_callback(self, payload, result_data): ...

    def on_error_callback(self, payload, exception_raised): ...

    def on_message_callback(self, payload): ...

    def process_task(self, process_index):
        print(f'Launching EMQ Message processor Thread #{process_index} ...', flush=True)
        try:
            print(f'EMQ Message processor Thread #{process_index} is listen now.', flush=True)

            while True:
                found_data = False
                while not found_data:
                    obj = self.queue.get()
                    if obj is not None:
                        found_data = True
                try:
                    print(f'Executing OnMessage callback on MQP-Thread #{process_index}/{len(self.processes)}', flush=True)
                    result_data = self.on_message_callback(payload=obj)
                    self.on_success_callback(payload=obj, result_data=result_data)
                    self.queue.task_done()
                except Exception as e:
                    if isinstance(e, KeyboardInterrupt):
                        # stop tread
                        raise KeyboardInterrupt(f'{e}')
                    else:
                        self.on_error_callback(payload=obj, exception_raised=e)
        except KeyboardInterrupt:
            print(f'EMQ Message processor Thread #{process_index} stop signal.', flush=True)
            exit(0)
        except Exception as e:
            print(f'EMQ Message processor Thread #{process_index} abnormal finalization signal. {e}', flush=True)
            exit(1)

    def terminate(self):
        """Wait until queue is empty and terminate processes """
        self.queue.join()
        for i, p in enumerate(self.processes):
            if isinstance(p, mp.context.Process):
                logger.info(f'Stopping thread #{i} ...')
                if p.is_alive():
                    p.terminate()
                logger.info(f'Thread #{i} successfully closed')

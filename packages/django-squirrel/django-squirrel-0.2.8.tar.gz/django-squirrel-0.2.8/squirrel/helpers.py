"""
Squirrel Helpers
"""
from logging import getLogger as getLocalLogger
import multiprocessing as mp

logger = getLocalLogger(__name__)


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

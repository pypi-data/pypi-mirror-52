"""
Squirrel loops

"""
from logging import getLogger as getLocalLogger
import time

logger = getLocalLogger(__name__)


class Loop:
    """Loop"""
    _args = list()
    _kwargs = dict()
    name = 'loop-base'
    auto_loop = True
    iteration_delay = 1  # Seconds

    def __init__(self, auto_start=False, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self.initialize()
        if auto_start:
            self.loop()

    def initialize(self):
        """Initialize loop"""

    def loop(self, *args, **kwargs):
        """Core-Loop"""

    def start(self):
        """Start looping"""
        try:
            if not self.auto_loop:
                while True:
                    logger.info('AUTO_LOOP Disabled')
                    self.loop(*self._args, **self._kwargs)
                    logger.warning('Recycling loop ...')
                    time.sleep(self.iteration_delay)
                    logger.debug('Restarting loop ...')
            else:
                logger.info('AUTO_LOOP Enable')
                self.loop(*self._args, **self._kwargs)
        except KeyboardInterrupt:
            logger.info('Normal close')
        except Exception as e:
            logger.critical(f'Abnormal finalization. Loop raises: {e.__class__.__name__}({e})')

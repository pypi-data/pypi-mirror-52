"""
Squirrel Drones
---

"""
from logging import getLogger as getLocalLogger

logger = getLocalLogger(__name__)


class Drone:
    """Drone"""
    process_class = None
    __process__ = None
    logger = None

    def __init__(self, auto_go=False, process_class=None, *args, **kwargs):
        logger.info(f'Deploying drone {self.name}')
        self.process_class = process_class or self.process_class
        if self.process_class is None:
            raise TypeError(f'Empty process_class is not allowed')
        self.deploy(*args, **kwargs)
        if auto_go:
            self.go()

    @property
    def name(self):
        """Get drone var_name"""
        return f'{self.__class__.__name__}'

    @property
    def is_deployed(self) -> bool:
        """Drone is deployed?"""
        return self.__process__ is not None

    def deploy(self, *args, **kwargs):
        """Deploy drone"""
        self.__process__ = self.process_class(*args, **kwargs)

    def go(self):
        """Start drone work"""
        if self.is_deployed:
            self.__process__.start()
        else:
            raise RuntimeError('Drone not deployed')



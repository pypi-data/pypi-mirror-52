"""
Squirrel Process
"""
from logging import getLogger as getLocalLogger
from squirrel.loops import Loop

logger = getLocalLogger(__name__)


class Process:
    """Process"""
    name = 'process'
    loop_class = None
    __loop__ = None

    def __init__(self, loop_class=None, *args, **kwargs):
        self.loop_class = loop_class or self.loop_class
        if self.loop_class is None:
            raise TypeError('loop_class is not properly configured. Empty loop_class is not allowed')
        if not isinstance(self.loop_class, Loop):
            raise TypeError(f'{self.loop_class.__class__.__name__} loop_class is not supported')
        self.create(*args, **kwargs)

    def create(self, *args, **kwargs):
        """Create process"""
        self.__loop__ = self.loop_class(*args, **kwargs)

    def pre_check(self):
        """Pre runs checks"""
        if self.__loop__ is None:
            raise ValueError('Loop creation fails. Loop.raise_event() aborted')

    def run(self):
        """Run process"""
        self.pre_check()
        self.__loop__.start()




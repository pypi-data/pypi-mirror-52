# Squirrel Events
from logging import getLogger as getLocalLogger
from importlib import import_module
from django.conf import settings

logger = getLocalLogger(__name__)


class Event:
    """Event base"""
    name = 'unnamed-base-hook'

    def __init__(self, name=None, callback=None):
        """hook constructor"""
        logger.debug(f'Creating hook "{self.name}"')
        self.name = name or self.name
        if callable(callback):
            self.callback = callback
        logger.debug(f'Event "{self.name}" successfully created')

    def callback(self, **arguments):
        """User callback"""
        logger.debug(f'{self}')
        logger.debug(f'{arguments}')

    def __str__(self):
        return f'+ {self.name}: "{self.callback.__doc__}".'


class EventsProcessor:
    """Event processor base"""
    __events__: list = None
    name = 'Unnamed-events-processor'
    initialized = False

    @staticmethod
    def __normalize_name__(name, is_var=True) -> str:
        if not isinstance(name, str):
            raise TypeError(f'Name should be an STR instance. '
                            f'"{name.__class__.__name__}" is not supported')
        if len(name) < 1:
            raise ValueError('"Name" argument length should be greater than zero')
        chars_white_list = 'qwertyuiopasdfghjklzxcvbnm_1234567890'
        wildcard = '_'
        cleaned_name = ''.join([c if c in chars_white_list else wildcard for c in name.lower()])
        if is_var:
            return cleaned_name.upper()
        else:
            return cleaned_name

    def __init__(self, name=None, initial_hooks=None, self_initialized=True):
        self.__events__ = initial_hooks or self.__events__ or []
        logger.debug(f'Starting Squirrel "{self.name}" Hooks Processor ... ')
        self.name = name or self.name
        if self_initialized:
            self.initialize()
        logger.debug(f'Event processor "{self.name}" was successfully started!')

    def on_failure(self, exception_raised, propagate=True):
        """On error callback"""
        logger.exception(f'"{self.name}" Fails. '
                         f'Exception Raised: {exception_raised.__class__.__name__}. '
                         f'{exception_raised}')
        if propagate:
            raise exception_raised.__class__(f'{exception_raised}')

    def import_events_callbacks(self):
        source_var_name = self.__normalize_name__(self.name.upper())
        logger.debug(f'Searching Events for "{source_var_name}" ...')
        sources = getattr(settings, source_var_name, [])
        if not isinstance(sources, list):
            raise TypeError(f'{source_var_name} should be an list instance. '
                            f'"{sources.__class__.__name__}" is not supported')
        if len(sources) == 0:
            logger.warning(f'Warning "{self.name}" hook processor is empty!')
            return False
        for source in sources:
            if not isinstance(source, str):
                raise TypeError(f'source path should be an str instance. '
                                f'"{source.__class__.__name__}" is not supported')
            try:
                _m = import_module(source)
                if not hasattr(_m, source_var_name.lower()):
                    raise ImportError(f'{source_var_name.lower()} does not search on {source}')
                _h = getattr(_m, source_var_name.lower())
                if not isinstance(_h, list):
                    raise TypeError('EventsList should be an LIST instance')
                self.__events__ += _h
            except ModuleNotFoundError:
                self.on_failure(ImportError(f'"{source}" not found'))
            except Exception as e:
                self.on_failure(exception_raised=e)
        logger.debug(f'{self}\nSuccessfully loaded.')

    def initialize(self):
        try:
            self.import_events_callbacks()
            if not all([isinstance(hook, Event) for hook in self.__events__]):
                raise TypeError('Unsupported Event class')
            self.initialized = True
        except Exception as exception_raised:
            self.on_failure(exception_raised=exception_raised)

    def raise_event(self, **arguments):
        """Run __events__ callbacks"""
        if not self.initialized:
            self.initialize()
        # Run all hooks
        logger.debug(f'Executing EventsProcessor "{self.name}" ...')
        try:
            for event in self.__events__:
                logger.debug(f'[*] Running callback for "{event.name}" ...')
                event.callback(**arguments)
                logger.debug(f'[*] "{event.name}" ends [OK]')
            logger.debug(f'"{self.name}" ends [OK]')
        except Exception as e:
            self.on_failure(exception_raised=e)

    def __str__(self) -> str:
        _hooks_as_str = '\n'.join([f'{h}' for h in self.__events__])
        return f'HooksProcessor({len(self.__events__)}): "{self.name}"\n{_hooks_as_str}'


class OnInitEventsProcessor(EventsProcessor):
    """OnInit event processor"""
    name = 'on-init-events'


class OnCloseEventsProcessor(EventsProcessor):
    """OnClose event processor"""
    name = 'on-close-events'


class OnFailureCloseEventsProcessor(EventsProcessor):
    """OnFailureClose events processor"""
    name = 'on-failure-close-events'


logger.debug('---------- Hooks ... ----------')
# On init hook processor instance
on_init_tasks = OnInitEventsProcessor()
# On close hook processor instance
on_close_tasks = OnCloseEventsProcessor()
# On failure close hook processor instance
on_abnormal_close_tasks = OnFailureCloseEventsProcessor()

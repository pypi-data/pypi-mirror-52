from logging import getLogger as getLocalLogger
from importlib import import_module
from squirrel.views import \
    PingView as Ping, \
    InfoView as Info

from squirrel.routes import Route, Router
from django.conf import settings

logger = getLocalLogger(__name__)

# Get main routes
logger.debug('---------- Routes ... ----------')
logger.debug('Loading ROOT_URLCONF ...')
main_router = getattr(settings, 'SQUIRREL_ROOT_URLCONF', '__demo__')

logger.debug('Loading Default Routes ...')
default_routes = [
    # Default Endpoints
    Route(path=f'/{settings.INCOMING_QUEUE}/ping', view_class=Ping, name='ping'),
    Route(path=f'/{settings.INCOMING_QUEUE}/info', view_class=Info, name='info'),
]
router = Router()
if main_router == '__demo__':
    router.add_routes(default_routes)
    setattr(settings, 'SQUIRREL_DEMO', True)
    logger.warning(f'Achtung! Running in DEMO mode. URL file: "{__name__}".\n'
                   f'Enable Routes:\n'
                   f'{router}')
else:
    logger.debug(f'Running in CUSTOM mode. URL full path: "{main_router}"')
    try:
        project, py_file, _router = main_router.split('.')
        module_path = f'{project}.{py_file}'
        router_module = import_module(module_path)
        if hasattr(router_module, _router):
            logger.debug(f'Router founded. Router path: "{module_path}".\n'
                         f'Enable Routes:\n'
                         f'{getattr(router_module, _router)}')
        else:
            err_msg = f'Router "{router}" does not search!'
            logger.exception(err_msg)
            raise ValueError(err_msg)
    except ModuleNotFoundError:
        err_msg = f'Root URLConf "{main_router}" not found!'
        logger.exception('Root URLConf not found')
        raise ValueError(err_msg)

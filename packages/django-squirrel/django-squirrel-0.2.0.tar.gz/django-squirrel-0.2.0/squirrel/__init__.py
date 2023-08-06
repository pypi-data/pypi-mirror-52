from squirrel.settings import local_vars
from django.conf import settings
from importlib import import_module


def parse_middleware_path(middleware_path) -> tuple:
    try:
        app, module, middleware = middleware_path.split('.')
    except ValueError:
        raise IOError('Bad middleware path. Please re check you settings!')
    return f'{app}.{module}', middleware


def squirrel_required_middleware(middleware_classes=None):
    """Middleware required loader """
    required_middleware_classes_list = []
    if isinstance(middleware_classes, list):
        for middleware_class in middleware_classes:
            path, middleware = parse_middleware_path(middleware_class)
            try:
                base_module = import_module(path)
            except ModuleNotFoundError:
                raise ModuleNotFoundError(f'App {path} not found')
            if hasattr(base_module, middleware):
                required_middleware_classes_list.append(getattr(base_module, middleware))
            else:
                raise ImportError(f'Middleware {middleware} not found')
    return required_middleware_classes_list


# Initialize squirrel configs
for name, value in local_vars.items():
    forced = False
    # Pre loaders
    if name.lower() == 'squirrel_required_middleware':
        value = squirrel_required_middleware(middleware_classes=value)
        forced = True
    if not hasattr(settings, name) or forced:
        setattr(settings, name, value)

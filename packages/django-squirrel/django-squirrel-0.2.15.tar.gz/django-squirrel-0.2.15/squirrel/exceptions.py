from logging import getLogger as getLocalLogger

logger = getLocalLogger(__name__)


class CustomException(Exception):
    """Custom Exception"""
    custom_message = 'Custom message'

    @staticmethod
    def render_args(args) -> str:
        if not isinstance(args, (dict, list)):
            return f'.' + f' {args}' if args is not None else ''
        if len(args) > 0:
            return '. ' + ', '.join(args if isinstance(args, list) else [f'{k}={v}' for k, v in args.items()])
        return ''

    def render_message(self, _custom_message=None, *args, **kwargs) -> str:
        rendered_args = self.render_args(args=args)
        rendered_kwargs = self.render_args(args=kwargs)
        message = _custom_message or self.custom_message or ""
        return f'{message}{rendered_args}{rendered_kwargs}'

    def __init__(self, _custom_message=None, *args, **kwargs):
        _message = self.render_message(_custom_message=_custom_message, *args, **kwargs)
        super().__init__(_message)


class NotFound(CustomException):
    """Not found exception"""
    custom_message = 'Object not found'


class BadRequest(CustomException):
    """Bad request exception"""
    custom_message = 'Bad Request'


class InternalError(CustomException):
    """Internal Error exception"""
    custom_message = 'Internal Error'


class MethodNotFound(NotFound):
    """Method not found"""
    custom_message = 'Method Not found'


class URLNotFound(NotFound):
    """URL not found"""
    custom_message = 'URL not found'


class MiddlewareNotFound(NotFound):
    """Middleware not found"""
    custom_message = 'Middleware not found'


class NotFocusedView(CustomException):
    """Out of focus exception"""
    custom_message = 'Working on FOCUS mode. '

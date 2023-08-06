from squirrel.exceptions import URLNotFound, BadRequest
from logging import getLogger as getLocalLogger
from squirrel.publishers import PublisherMixin
from squirrel.responses import Response
from squirrel.contexts import Context
from django.db import connections
from squirrel.views import View

logger = getLocalLogger(__name__)


class Route:
    name = 'UnnamedRoute'
    path = None
    view = None

    def __init__(self, path=None, view_class=None, name=None):
        self.name = name or self.name
        self.path = path
        self.view = view_class
        self.__is_valid__()

    def __is_valid__(self) -> bool:
        """Self route validation"""
        if any([prop is None for prop in [self.path, self.view]]):
            raise ValueError('Bad route configuration')
        if not isinstance(self.path, str) or self.path == '':
            raise ValueError('Invalid Path')
        if super(self.view) is View:
            raise TypeError(f'{self.view.__name__} is not supported')
        return True

    def __str__(self) -> str:
        """
        Route as str
        ---
        Example:

            route_name: [/path/to/view -> ViewName]
        """
        return f'{self.name}: [{self.path} -> {self.view.__name__}]'


class Router(PublisherMixin):
    """Router Squirrel routes"""
    __routes__ = []

    @property
    def routes(self):
        return [route.path for route in self.__routes__]

    def export_router(self) -> list:
        return self.__routes__

    def get_route_index(self, route):
        if self.exists_route(route):
            return self.routes.index(route)
        raise URLNotFound(route)

    def exists_route(self, route) -> bool:
        return route in self.routes

    def validate_route(self, route):
        if not isinstance(route, Route):
            raise ValueError(f'{route.__class__.__name__} is nor supported as route')
        routes_names = [route.name for route in self.__routes__]
        routes_paths = [route.path for route in self.__routes__]
        if route.path in routes_paths:
            raise ValueError(f'Duplicated route PATH. {route} is already added to routes. '
                             f'Route index: {self.__routes__.index(route)}')
        if route.name in routes_names:
            raise ValueError(f'Duplicated route NAME. {route} is already added to routes. '
                             f'Route index: {self.__routes__.index(route)}')
        return route

    def add_routes(self, route_list):
        if not isinstance(route_list, list):
            raise ValueError('{} is not supported as Routes list'.format(route_list.__class__.__name__))
        for route in route_list:
            self.__routes__.append(self.validate_route(route))

    def submit_request(self, request) -> Response:
        """Submit request to routes"""
        # Recycle all db connection
        connections.close_all()
        processed_response = self.process_request(request=self.middleware(request=request))
        return processed_response

    def process_request(self, request) -> Response:
        view_class = self.__routes__[self.get_route_index(request.url)].view
        logger.debug(f'View Class invoked: {view_class.__name__}'
                     f'Hit URL: {request.url}'
                     f'Class view successfully obtenied')
        if isinstance(request.params, list):
            context = Context(*request.params)
        elif isinstance(request.params, dict):
            context = Context(**request.params)
        else:
            raise BadRequest('Invalid context')
        logger.info(f'Context successfully retrieved.\n'
                    f'Context: {context}.\n'
                    f'Request: {request}.')
        _view = view_class(request=request, context=context)
        logger.info('View successfully rendered')
        response = _view.render()
        logger.debug('Response created')
        if response.send_payload:
            # submit payload
            logger.debug(f'Sending payload ...'
                         f'Routing-key "{response.routing_key}"')
            response.routing_key = self.queue_name
            logger.debug(f'Response URL: "{response.url}".\n'
                         f'Response Method: "{response.method}".\n'
                         f'Response Params: "{response.params}".')
            self.publish(response=response)
            logger.info('Payload successful sent')
        logger.info(f'Request {response} successfully processed')
        return response

    def __str__(self) -> str:
        available_routes = '\n'.join([f'+ {r.name}: ({r.path} -> {r.view.__name__})' for r in self.__routes__])
        return f'{available_routes}'

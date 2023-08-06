from squirrel.settings import local_vars
from django.conf import settings


class SquirrelCommandHelper:
    """Squirrel command helper"""

    @staticmethod
    def dj_var_to_flag(var_name: str) -> str:
        if not isinstance(var_name, str):
            raise TypeError
        wildcard = '-'
        allowed_chars = 'qwertyuiopasdfghjklzxcvbnm1234567890' + wildcard
        var_name_f = var_name.lower()\
            .replace('rabbit_mq', '')\
            .replace('squirrel', '')
        var_name = ''.join([c if c in allowed_chars else wildcard for c in var_name_f])
        if not var_name.startswith('--'):
            var_name = f'--{var_name}'
        return var_name

    def default_arguments(self, **default):
        virtual_host = options.get('virtual_host')
        incoming_queue = options.get('incoming_queue')
        outgoing_queue = options.get('outgoing_queue')
        hostname = options.get('hostname')
        username = options.get('username')
        password = options.get('password')
        port = options.get('port')
        setattr(settings, 'RABBIT_MQ_PORT', port)
        setattr(settings, 'RABBIT_MQ_HOSTNAME', hostname)
        setattr(settings, 'RABBIT_MQ_USERNAME', username)
        setattr(settings, 'RABBIT_MQ_PASSWORD', password)
        setattr(settings, 'INCOMING_QUEUE', incoming_queue)
        setattr(settings, 'OUTGOING_QUEUE', outgoing_queue)
        setattr(settings, 'RABBIT_MQ_VIRTUAL_HOST', virtual_host)
        return {}

    def extra_arguments(self, **arguments): ...
    def build_arguments(self, **arguments): ...

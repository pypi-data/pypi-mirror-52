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

    @staticmethod
    def default_arguments(**default):
        setattr(settings, 'RABBIT_MQ_PORT', default.get('port'))
        setattr(settings, 'RABBIT_MQ_HOSTNAME', default.get('hostname'))
        setattr(settings, 'RABBIT_MQ_USERNAME', default.get('username'))
        setattr(settings, 'RABBIT_MQ_PASSWORD', default.get('password'))
        setattr(settings, 'INCOMING_QUEUE', default.get('incoming_queue'))
        setattr(settings, 'OUTGOING_QUEUE', default.get('outgoing_queue'))
        setattr(settings, 'RABBIT_MQ_VIRTUAL_HOST', default.get('virtual_host'))

    def extra_arguments(self, **arguments): ...
    def build_arguments(self, **arguments): ...

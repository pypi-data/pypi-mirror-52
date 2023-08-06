from squirrel.settings import local_vars
from django.conf import settings


# Initialize squirrel configs
for var_name, value in local_vars.items():
    _ff = getattr(settings, 'FORCED_SQUIRREL_DEFAULT_SETTING', False)
    forced = _ff if isinstance(_ff, bool) else False
    if not hasattr(settings, var_name):
        # Create or Update settings header `var_name` with `value`
        setattr(settings, var_name, value)

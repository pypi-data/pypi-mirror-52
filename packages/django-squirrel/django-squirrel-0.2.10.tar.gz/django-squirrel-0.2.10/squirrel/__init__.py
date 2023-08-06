from squirrel.settings import local_vars
from django.conf import settings


# Initialize squirrel configs
for var_name, value in local_vars.items():
    _ff = settings.get('FORCED_SQUIRREL_DEFAULT_SETTING', False)
    forced = _ff if isinstance(_ff, bool) else False
    if settings.get(var_name) is not None or forced:
        # Create or Update settings key `var_name` with `value`
        setattr(settings, var_name, value)

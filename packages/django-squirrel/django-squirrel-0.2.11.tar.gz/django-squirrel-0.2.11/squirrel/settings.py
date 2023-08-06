"""
Local settings
"""

local_vars = {
    'RABBIT_MQ_HOSTNAME': 'localhost',
    'RABBIT_MQ_USERNAME': 'guest',
    'RABBIT_MQ_PASSWORD': 'guest',
    'RABBIT_MQ_PORT': 5672,
    'RABBIT_MQ_VIRTUAL_HOST': '/',
    # API connection
    'INCOMING_QUEUE': 'incoming',
    'OUTGOING_QUEUE': 'outgoing',
    'SQUIRREL_MIDDLEWARE': [],
    'SQUIRREL_VERSION': '0.2.10',
    'SQUIRREL_CODENAME': 'katana',
    'SQUIRREL_RELEASE_DATE': '17092019',
}

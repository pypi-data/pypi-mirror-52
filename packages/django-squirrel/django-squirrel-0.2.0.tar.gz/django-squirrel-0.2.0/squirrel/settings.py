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
    'INCOMING_QUEUE': 'api',
    'OUTGOING_QUEUE': 'blockchain',
    'SQUIRREL_REQUIRED_MIDDLEWARE': ['squirrel.middleware.CommonMiddleware',
                                     'squirrel.middleware.SecurityValidationCheck'],
    'SQUIRREL_MIDDLEWARE': [],
    'TOKEN_ADDRESS': None,
    'TOKEN_ABI_PATH': 'contract_abi/token.abi.json',
    'TOKEN_SIGNER_PK': 'B8F68BBEA8C26E384B488AACBF0445E84C60982C15DEE21259AD1218DEC0FAC3',

}

import os
import boto3
ENVIRONMENT = os.environ.get("ENVIRONMENT", 'local')
DB_PASSWORD = None
FACEBOOK_TOKEN = None
SECRET_KEY = None
parameters = dict()


if os.environ.get('ENCRYPTED_FACEBOOK_TOKEN'):
    parameters[os.environ.get('ENCRYPTED_FACEBOOK_TOKEN')] = 'FACEBOOK_TOKEN'
else:
    FACEBOOK_TOKEN = os.environ.get('FACEBOOK_TOKEN')

if os.environ.get('ENCRYPTED_DJANGO_SECRET_KEY'):
    parameters[os.environ.get('ENCRYPTED_DJANGO_SECRET_KEY')] = 'SECRET_KEY'
else:
    SECRET_KEY = 'kzv$s=4j$y5hkx4$9kai799(kf$ac^rix=t_0b149*wx!iit+t'

if os.environ.get('ENCRYPTED_CRAFTY_DB_PASSWORD'):
    parameters[os.environ.get('ENCRYPTED_CRAFTY_DB_PASSWORD')] = 'DB_PASSWORD'
else:
    DB_PASSWORD = 'test'

ssm = boto3.client('ssm')

stored_parameters = ssm.get_parameters(
    Names=parameters.keys(),
    WithDecryption=True
)

for param in stored_parameters.get('Parameters', list()):
    if parameters[param['Name']] == 'FACEBOOK_TOKEN':
        FACEBOOK_TOKEN = param['Value']
    elif parameters[param['Name']] == 'SECRET_KEY':
        SECRET_KEY = param['Value']
    elif parameters[param['Name']] == 'DB_PASSWORD':
        DB_PASSWORD = param['Value']

BUCKETS = dict(
    default=os.environ.get('CRAFTY_DEFAULT_BUCKET', "craftybot"),
    static=os.environ.get('CRAFTY_STATIC_BUCKET', "craftybot"),
)
S3_REGION = os.environ.get('S3_REGION', 'us-east-1')
DOMAIN = os.environ.get('DOMAIN', 'https://acraftybot.com')
DB_USER = os.environ.get('CRAFTY_DB_USER', 'test')


DATABASES = dict(
    default=dict(
        ENGINE=os.environ.get('CRAFTY_DB_ENGINE', "django.db.backends.postgresql"),
        NAME=os.environ.get('CRAFTY_DB_NAME', 'craftydb'),
        USER=DB_USER,
        PASSWORD=DB_PASSWORD,
        HOST=os.environ.get('CRAFTY_DB_HOST', 'localhost'),
        PORT=int(os.environ.get('CRAFTY_DB_PORT', '5432')),
    )
)

CELERY_BROKER_URL = "sqs://"
broker_transport_options = {
    'region': S3_REGION,
    'queue_name_prefix': 'craftybot-',
    'polling_interval': 20
}
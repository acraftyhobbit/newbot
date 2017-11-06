import os
import boto3
from base64 import b64decode
ENVIRONMENT = os.environ.get("ENVIRONMENT", 'local')

print(os.environ.get('ENCRYPTED_FACEBOOK_TOKEN'))

if os.environ.get('ENCRYPTED_FACEBOOK_TOKEN'):
    FACEBOOK_TOKEN = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(os.environ.get('ENCRYPTED_FACEBOOK_TOKEN'))
    )['Plaintext'].decode('utf-8')
else:
    FACEBOOK_TOKEN = os.environ.get('FACEBOOK_TOKEN')

if os.environ.get('ENCRYPTED_DJANGO_SECRET_KEY'):
    SECRET_KEY = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(os.environ.get('ENCRYPTED_DJANGO_SECRET_KEY'))
    )['Plaintext'].decode('utf-8')
else:
    SECRET_KEY = 'kzv$s=4j$y5hkx4$9kai799(kf$ac^rix=t_0b149*wx!iit+t'

BUCKETS = dict(
    default=os.environ.get('CRAFTY_DEFAULT_BUCKET', "craftybot"),
    static=os.environ.get('CRAFTY_STATIC_BUCKET', "craftybot"),
)

S3_REGION = os.environ.get('S3_REGION', 'us-east-1')
DOMAIN = os.environ.get('DOMAIN', 'https://9b8fb740.ngrok.io')

if os.environ.get('ENCRYPTED_CRAFTY_DB_PASSWORD'):
    DB_PASSWORD = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(os.environ.get('ENCRYPTED_CRAFTY_DB_PASSWORD'))
    )['Plaintext'].decode('utf-8')
else:
    DB_PASSWORD = 'test'

if os.environ.get('ENCRYPTED_CRAFTY_DB_USER'):
    DB_USER = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(os.environ.get('ENCRYPTED_CRAFTY_DB_USER'))
    )['Plaintext'].decode('utf-8')
else:
    DB_USER = 'test'

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
import os
import boto3
ENVIRONMENT = os.environ.get("ENVIRONMENT", 'local')

FACEBOOK_TOKEN = os.environ.get('ENCRYPTED_FACEBOOK_TOKEN')
DB_PASSWORD = os.environ.get('ENCRYPTED_CRAFTY_DB_PASSWORD', 'test')
SECRET_KEY = os.environ.get('ENCRYPTED_DJANGO_SECRET_KEY', 'kzv$s=4j$y5hkx4$9kai799(kf$ac^rix=t_0b149*wx!iit+t')

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

CELERY_BROKER_URL = 'redis://{0}:6379/0'.format(os.environ.get('CELERY_BROKER', 'localhost'))
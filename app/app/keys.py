import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", 'local')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'kzv$s=4j$y5hkx4$9kai799(kf$ac^rix=t_0b149*wx!iit+t')
FACEBOOK_TOKEN = os.environ.get('FACEBOOK_TOKEN')

BUCKETS = dict(
    default=os.environ.get('CRAFTY_DEFAULT_BUCKET', "craftybot"),
    static=os.environ.get('CRAFTY_STATIC_BUCKET', "craftybot"),
    user=os.environ.get('CRAFTY_USER_BUCKET', "craftybot"),
)

S3_REGION = os.environ.get('S3_REGION', 'us-east-1')
DOMAIN = os.environ.get('DOMAIN', 'https://9b8fb740.ngrok.io')
DATABASES = dict(
    default=dict(
        ENGINE=os.environ.get('CRAFTY_DB_ENGINE', "django.db.backends.postgresql"),
        NAME=os.environ.get('CRAFTY_DB_NAME', 'craftydb'),
        USER=os.environ.get('CRAFTY_DB_USER', 'test'),
        PASSWORD=os.environ.get('CRAFTY_DB_PASSWORD', 'test'),
        HOST=os.environ.get('CRAFTY_DB_HOST', 'localhost'),
        PORT=int(os.environ.get('CRAFTY_DB_PORT', '5432')),
    )
)

# TODO switch to SQS
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'localhost')
if "redis://" not in CELERY_BROKER_URL:
    CELERY_BROKER_URL = 'redis://{0}:6379/0'.format(CELERY_BROKER_URL)

CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND', 'localhost')

if "cache+memcached://" not in CELERY_RESULT_BACKEND:
    CELERY_RESULT_BACKEND = 'cache+memcached://{0}:11211'.format(CELERY_RESULT_BACKEND)

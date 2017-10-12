import os
ENVIRONMENT = os.environ.get("ENVIRONMENT", 'local')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'kzv$s=4j$y5hkx4$9kai799(kf$ac^rix=t_0b149*wx!iit+t')
FACEBOOK_TOKEN = os.environ.get('FACEBOOK_TOKEN')

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
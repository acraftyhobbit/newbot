#!/bin/bash
source /env/bin/activate
cd /apps/app/
exec gunicorn app.wsgi:application \
    --config /apps/deployment/conf/gunicorn_settings.py &
exec service nginx start
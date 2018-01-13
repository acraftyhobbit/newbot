#!/usr/bin/env bash
exec supervisord
exec supervisorctl reread
exec supervisorctl update
exec service postgresql start
exec source env/bin/activate
exec psql -U root -d postgres -c 'create database craftydb'
cd /apps/app/
exec python /apps/app/manage.py migrate
exec gunicorn app.wsgi:application \
    --config /apps/deployment/conf/gunicorn_settings.py &
exec service nginx start
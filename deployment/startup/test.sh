#!/usr/bin/env bash
cd /apps/app/
source /env/bin/activate
service postgresql start
exec supervisord &
python manage.py test
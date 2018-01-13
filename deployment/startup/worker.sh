#!/usr/bin/env bash
exec service postgresql start
exec source env/bin/activate
cd /apps/app/
exec celery --app=app worker --loglevel=INFO --concurrency=1 -n craftybot-%h
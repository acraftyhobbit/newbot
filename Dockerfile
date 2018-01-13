FROM perrystallings/ubuntu-python3.5.2-django-celery-test:latest

RUN apt-get update && \
    apt-get install -y nginx python-pip

COPY . /apps/.

RUN cp /apps/deployment/conf/nginx.conf /etc/nginx/sites-available/ && \
    ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled && \
    echo "daemon off;" >> /etc/nginx/nginx.conf

EXPOSE 8000

RUN python -m virtualenv env -p python3.5 && \
    . env/bin/activate && \
    pip install --upgrade pip && \
    pip install -r /apps/requirements.txt

RUN chmod +x /apps/deployment/startup/app.sh && \
    chmod +x /apps/deployment/startup/local.sh && \
    chmod +x /apps/deployment/startup/test.sh && \
    chmod +x /apps/deployment/startup/worker.sh
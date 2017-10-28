FROM perrystallings/ubuntu-python3.5.2:latest

EXPOSE 6379 11211 80 5432

RUN mkdir /apps && \
    mkdir /apps/files && \
    mkdir /apps/logs

COPY . /apps/.

RUN python -m virtualenv /apps/env -p python3.5 && \
    . /apps/env/bin/activate && \
    pip install --upgrade pip && \
    pip install -q -r /apps/deployment/requirements.txt
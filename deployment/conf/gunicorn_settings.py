import multiprocessing

bind = "unix:django_app.sock"
#worker_class = 'aiohttp'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '-'
errorlog = '-'
loglevel = 'info'
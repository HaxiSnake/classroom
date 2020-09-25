import multiprocessing

bind = '0.0.0.0:8000'
backlog = 512
chdir = '/app'
timeout = 30
worker_class = 'gthread'

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
loglevel = 'debug'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = "/var/log/gunicorm_access.log"
errorlog = "/var/log/gunicorn_error.log"

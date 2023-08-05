import os
bind = '0.0.0.0:8080'
workers = 4
backlog = 2048
debug = False
proc_name = 'gunicorn.pid'
pidfile = 'gunicorn.pid'
logfile = 'debug.log'
loglevel='debug'
accesslog='gunicorn-accesslog.log'
errorlog='gunicorn-errorlog.log'
[uwsgi]
socket = 127.0.0.1:8005
chdir = "/home/ubuntu/dbhub/"
wsgi-file = dbhub/wsgi.py
master = true
processes = 2
harakiri = 60
limit-as = 1000
max-requests = 5000
single-interpreter = true
enable-threads = true
env = DJANGO_SETTINGS_MODULE="project.settings.prod"
virtualenv = "/home/ubuntu/.virtualenvs/dbhub"

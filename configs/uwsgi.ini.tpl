[uwsgi]
http = {eth0.ipv4.address}:8005
chdir = /data/www/{project_name}/
wsgi-file = {project_name}/wsgi.py
master = true
processes = 2
harakiri = 60
limit-as = 1000
max-requests = 5000
single-interpreter = true
enable-threads = true
env = DJANGO_SETTINGS_MODULE="dbhub.settings.{env}"
virtualenv = "/data/www/{project_name}/venv/"

[uwsgi]
socket = {eth0.ipv4.address}:port
chdir = "/data/www/{ project_name }/"
wsgi-file = { project_name }/wsgi.py
master = true
processes = 2
harakiri = 60
limit-as = 1000
max-requests = 5000
single-interpreter = true
enable-threads = true
env = DJANGO_SETTINGS_MODULE="project.settings.{ env }"
virtualenv = "/data/www/{ project_name }/venv/" 

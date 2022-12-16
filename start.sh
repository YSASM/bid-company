#!/bin/bash
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT
# /usr/bin/python3 /app/run.py
echo "[program:FlaskGunicornSupervisor]" >> /etc/supervisord.conf
echo "command=/usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api" >> /etc/supervisord.conf
echo "directory=/app  ;" >> /etc/supervisord.conf
echo "user=root      ;" >> /etc/supervisord.conf
echo "autostart=false   ;" >> /etc/supervisord.conf
echo "autorestart=false ;" >> /etc/supervisord.conf
echo "startretires=5   ;" >> /etc/supervisord.conf
supervisord -c /etc/supervisord.conf 
supervisorctl update
nohup supervisorctl start FlaskGunicornSupervisor >> log/run.log 2>&1
    
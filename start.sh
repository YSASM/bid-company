#!/bin/bash
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT
# /usr/bin/python3 /app/run.py
echo "[program:FlaskGunicornSupervisor]" >> /etc/supervisord.conf
echo "command=nohup /usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api >> log/run.log 2>&1" >> /etc/supervisord.conf
echo "directory=/app  ;" >> /etc/supervisord.conf
echo "user=root      ;" >> /etc/supervisord.conf
echo "autostart=false   ;" >> /etc/supervisord.conf
echo "autorestart=false ;" >> /etc/supervisord.conf
echo "startretires=5   ;" >> /etc/supervisord.conf
supervisord -c /etc/supervisord.conf 
supervisorctl update
supervisorctl start FlaskGunicornSupervisor
while [ true ];do
        sleep 86400000
    done
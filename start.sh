#!/bin/bash
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT
mv /app/status.sh /usr/bin/api_status
# /usr/bin/python3 /app/run.py
echo "[program:Flask]" >> /etc/supervisord.conf
echo "command=/usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api" >> /etc/supervisord.conf
echo "directory=/app  ;" >> /etc/supervisord.conf
echo "user=root      ;" >> /etc/supervisord.conf
echo "autostart=false   ;" >> /etc/supervisord.conf
echo "autorestart=false ;" >> /etc/supervisord.conf
echo "startretires=5   ;" >> /etc/supervisord.conf
echo "stdout_logfile = /app/log/run.log" >> /etc/supervisord.conf
supervisord -c /etc/supervisord.conf 
supervisorctl update
supervisorctl start Flask
while [ true ];do
        sleep 86400000
    done
#!/bin/bash
echo "[program:FlaskGunicornSupervisor]" >> /etc/supervisord.conf
echo "command=/usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api" >> /etc/supervisord.conf
echo "directory=/app  ;" >> /etc/supervisord.conf
echo "user=root      ;" >> /etc/supervisord.conf
echo "autostart=true   ;" >> /etc/supervisord.conf
echo "autorestart=true ;" >> /etc/supervisord.conf
echo "startretires=5   ;" >> /etc/supervisord.conf
supervisord -c /etc/supervisord.conf 
supervisorctl update
supervisorctl stop FlaskGunicornSupervisor
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT

if [ "$MODE"x == "test"x ];then
    while [ true ];do
        nohup supervisorctl start FlaskGunicornSupervisor >> log/run.log 2>&1
        sleep 86400000
    done
else
    exec supervisorctl start FlaskGunicornSupervisor >> log/run.log 2>&1
fi

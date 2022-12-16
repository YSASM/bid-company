#!/bin/bash
cp /usr/local/python-3.9/bin/gunicorn /usr/bin/
yum install supervisor
sudo touch /usr/etc/supervisor/conf.d/config.conf
sudo gedit /usr/etc/supervisor/conf.d/config.conf
echo "[program:FlaskGunicornSupervisor]\n
command=/usr/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api\n
directory=/app  ; \n
user=root      ; \n
autostart=true   ; \n
autorestart=true ; \n
startretires=5   ;" > /usr/etc/supervisor/conf.d/config.conf
supervisorctl update
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

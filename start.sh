#!/bin/bash
cp /usr/local/python-3.9/bin/gunicorn /usr/bin/
yum install supervisor
echo "[program:FlaskGunicornSupervisor]"
"command=/usr/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api"
"directory=/app  ;"
"user=root      ;"
"autostart=true   ;"
"autorestart=true ;"
"startretires=5   ;" >> /etc/supervisord.conf
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

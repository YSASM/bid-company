#!/bin/bash
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT
python3 /app/run.py
# echo "[program:FlaskGunicornSupervisor]" >> /etc/supervisord.conf
# if [ "$MODE"x == "test"x ];then
#     echo "command=nohup /usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api  >> log/run.log 2>&1" >> /etc/supervisord.conf
# else
#     echo "command=exec /usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api  >> log/run.log 2>&1" >> /etc/supervisord.conf
# fi
# echo "directory=/app  ;" >> /etc/supervisord.conf
# echo "user=root      ;" >> /etc/supervisord.conf
# echo "autostart=true   ;" >> /etc/supervisord.conf
# echo "autorestart=true ;" >> /etc/supervisord.conf
# echo "startretires=5   ;" >> /etc/supervisord.conf
# supervisord -c /etc/supervisord.conf 
# supervisorctl update

# if [ "$MODE"x == "test"x ];then
#     while [ true ];do
#         supervisorctl restart FlaskGunicornSupervisor
#         sleep 86400000
#     done
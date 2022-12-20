#!/bin/bash
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT
mv /app/status.sh /usr/bin/api_status
# 查询服务状态
mv /app/api_restart.sh /usr/bin/api_restart
# 重启api数据接口服务
mv /app/api_getid_restart.sh /usr/bin/api_getid_restart
# 重启api查询id服务
echo "[program:Api]" >> /etc/supervisord.conf
echo "command=/usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9252 run:api" >> /etc/supervisord.conf
echo "directory=/app  ;" >> /etc/supervisord.conf
echo "user=root      ;" >> /etc/supervisord.conf
echo "autostart=false   ;" >> /etc/supervisord.conf
echo "autorestart=false ;" >> /etc/supervisord.conf
echo "startretires=5   ;" >> /etc/supervisord.conf
echo "stdout_logfile = /app/log/api_run.log" >> /etc/supervisord.conf
echo "[program:Api_getid]" >> /etc/supervisord.conf
echo "command=/usr/local/python-3.9/bin/gunicorn -w 5 -b 0.0.0.0:9259 run:api_getid" >> /etc/supervisord.conf
echo "directory=/app  ;" >> /etc/supervisord.conf
echo "user=root      ;" >> /etc/supervisord.conf
echo "autostart=false   ;" >> /etc/supervisord.conf
echo "autorestart=false ;" >> /etc/supervisord.conf
echo "startretires=5   ;" >> /etc/supervisord.conf
echo "stdout_logfile = /app/log/api_getid_run.log" >> /etc/supervisord.conf
supervisord -c /etc/supervisord.conf 
supervisorctl update
supervisorctl start Api
# 启动api数据接口服务
supervisorctl start Api_getid
# 启动api查询id服务
if [ "$MODE"x == "test"x ];then
    while [ true ];do
        nohup /usr/bin/python3 main.py >> log/run.log 2>&1
        sleep 86400000
    done
else
    exec /usr/bin/python3 main.py >> log/run.log 2>&1
fi
# 启动管理面板
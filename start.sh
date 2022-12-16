#!/bin/bash 
set -x
ROOT=$(cd `dirname $0`; pwd)
cd $ROOT

if [ "$MODE"x == "test"x ];then
    while [ true ];do
        supervisorctl stop FlaskGunicornSupervisor
        nohup supervisorctl start FlaskGunicornSupervisor >> log/run.log 2>&1
        sleep 86400000
    done
else
    supervisorctl stop FlaskGunicornSupervisor
    exec supervisorctl start FlaskGunicornSupervisor >> log/run.log 2>&1
fi

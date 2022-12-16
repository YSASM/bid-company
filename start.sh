#!/bin/bash
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

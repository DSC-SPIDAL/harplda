#!/bin/bash
#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config


if [ $# -eq "1" -o $# -eq "2" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)

    chkinterval=100
    
    if [ $# -eq "2" ]; then
        chkinterval=$2
    fi
else
    echo "usage: make_lda.sh <slave file> <chkinterval>"
    exit 
fi

echo "make run_lda.xxx scripts as: chkinterval=$chkinterval"

#topics=10000
#iter=200
#alpha=100
#beta=0.01
#threads=64
if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

server_list=`cat server.list`
server_id=1

for host in ${hosts[*]}; do
    echo "echo \"run learntopics on $host\"" >  run_lda.$host
    echo "cd $ylda && source $ylda/setLibVars.sh" >> run_lda.$host
    #cmd="cd $work && $ylda/learntopics --topics=$topics --iter=$iter --servers=$server_list --alpha=$alpha --beta=$beta  --optimizestats=5000 --samplerthreads=$threads --chkptdir="/tmp" --chkptinterval=$chkinterval "
    cmd="cd $work && export GLOG_log_dir=$work && $ylda/learntopics --topics=$topics --iter=$iter --servers=$server_list --alpha=$alpha --beta=$beta  --optimizestats=5000 --samplerthreads=$threads  --chkptdir=$work --chkptinterval=$chkinterval "
    echo $cmd >> run_lda.$host
    ((server_id++))
done



#!/bin/bash
#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo "usage: build_logs.sh <slave file> "
    exit 
fi

#topics=1000
#iter=1000
if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

servercnt="${#hosts[*]}"

echo 'get all logs from clients'
server_id=0
file='learntopics'
for host in ${hosts[*]}; do
    scp $host:$work/$file.INFO $file.INFO.$host
    scp $host:$work/$file.WARNING $file.WARNING.$host
   ((server_id++))
done





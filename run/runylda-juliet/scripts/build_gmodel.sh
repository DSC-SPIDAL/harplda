#!/bin/bash
#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo "usage: build_gmodel.sh <slave file> "
    exit 
fi

#topics=1000
#iter=1000
if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

servercnt="${#hosts[*]}"

echo 'get all global_model from clients'
server_id=0
file='global_model'
for host in ${hosts[*]}; do
    scp $host:$work/$file $file.$server_id
    scp $host:$work/$file.hyper $file.hyper.$server_id
    cat $file.$server_id >> $file
   ((server_id++))
done





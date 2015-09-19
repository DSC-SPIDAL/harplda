#!/bin/bash
#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config


if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo "usage: make_modeldump.sh <slave file> "
    exit 
fi

#topics=1000
#iter=1000
if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

if [ ! -f "server.list" ];then
    echo "server.list not found, quit..."
    exit
fi


server_list=`cat server.list`
server_id=1
server_index=0
for host in ${hosts[*]}; do
    echo "echo \"run Merge_Topic_Counts on $host\"" >  run_modeldump.$host
    echo "cd $ylda && source $ylda/setLibVars.sh" >> run_modeldump.$host
    cmd="cd $work && $ylda/Merge_Topic_Counts --topics=$topics --clientid=$server_index --servers=$server_list --globaldictionary="lda.dict.dump.global" "
    echo $cmd >> run_modeldump.$host
    ((server_id++))
    ((server_index++))
done



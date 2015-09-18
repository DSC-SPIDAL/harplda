#!/bin/bash
#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo "Collect all nodes' interval models, merge them for convergence analysis"
    echo "usage: build_intervalmodel.sh <slave file> "
    exit 
fi

#topics=1000
#iter=1000
if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

servercnt="${#hosts[*]}"

echo 'get all files under working directories from clients'

# download all work files
mkdir -p local
mkdir -p global
cd local
server_id=0
for host in ${hosts[*]}; do
    scp -r $host:$work _tmp.$server_id
    mv _tmp.$server_id $host
   ((server_id++))
done
cd ..

# run merge
python ~/hpda/lda-test/src/preprocess/mergeTxtModeldata.py local global ../global_dict/global-dict.wordids

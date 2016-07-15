#!/bin/bash
#include the cluster setting

#
# Usage
#

homedir=`dirname $0`
. $homedir/conf/cluster_config

hostname="$homedir/conf/$cluster.hostname"
get_hosts="cat $homedir/conf/$cluster.hostname"
hosts=(`$get_hosts`)
echo "get server host from $hostname"

if [ $# -eq "1" ]; then
    appname=$1
else
    echo "Collect all nodes' interval models, merge them for convergence analysis"
    echo "usage: build_globalmodel.sh <appname>"
    exit 
fi

#topics=1000
#iter=1000
if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

### 8. save the result
mkdir -p result/$appname
cd result/$appname

servercnt="${#hosts[*]}"
echo "servercnt= "$servercnt

server_id=0
for host in ${hosts[*]}; do
    mkdir -p $host
    echo "scp -r $host:$workroot/work-$appname/* $host"
    scp -r $host:$workroot/work-$appname/* $host
   ((server_id++))
done

cd ../..


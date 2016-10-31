#!/bin/bash
#include the cluster setting
homedir=`dirname $0`/conf/
. $homedir/cluster_config
hostfile=$homedir/$cluster.hostname

hosts=(`cat $hostfile`)

if [ $# -ne "0" ]; then
    echo "usage: config_petuum.sh"
    exit 
fi

if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

id=1
for host in ${hosts[*]}; do
    if [ $id -eq '1' ]; then
        ((id++))
        host_list=$host
    else
        host_list=$host_list","$host
    fi
done

# mach.vm should be distributed first
#binsrc=/N/u/pengb/hpda/petuum/strads/apps/lda_release/bin/ldall
cexec mkdir -p $workroot
cexec mkdir -p $workroot/bin

echo 'host list='$host_list
echo 'workroot='$workroot
echo $ldall
cpush $ldall $workroot/bin/



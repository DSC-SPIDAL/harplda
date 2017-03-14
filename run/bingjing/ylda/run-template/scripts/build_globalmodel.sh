#!/bin/bash
#include the cluster setting

#
# Usage
#

homedir=`dirname $0`
. $homedir/cluster_config

if [ $# -eq "2" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
    appname=$2
else
    echo "Collect all nodes' interval models, merge them for convergence analysis"
    echo "usage: build_globalmodel.sh <slave file> <appname>"
    exit 
fi



#topics=1000
#iter=1000
if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

servercnt="${#hosts[*]}"


#
# step.1 download all worker's local dictioanry file
#
#echo 'get all dictionary files under working directories from clients'
#
mkdir -p localdicts
mkdir -p selectdicts 

cd localdicts
server_id=0
for host in ${hosts[*]}; do
    scp -r $host:$workroot/work-$appname/dict.wordids dict.wordids.$host
   ((server_id++))
done
cd ..

# run merge
python ~/hpda/lda-test/src/preprocess/distMergeTxtModel.py -mergedict localdicts selectdicts global-dict.wordids

#
# step.2 send select dicts back
#
cd selectdicts
for host in ${hosts[*]}; do
    scp -r dict.wordids.$host $host:$workroot/work-$appname/dict.wordids.$host
   ((server_id++))
done
cd ..


cexec "cd $workroot && mkdir -p select && python /N/u/pengb/hpda/lda-test/src/preprocess/distMergeTxtModel.py -extract work-$appname select work-$appname/dict.wordids."'$HOSTNAME'


#
# step.3 get back all selected model files
#
mkdir -p local
mkdir -p global

cd local
server_id=0
for host in ${hosts[*]}; do
    mkdir -p $host
    scp -r $host:$workroot/select/[0-9]* $host
   ((server_id++))
done
cd ..

python ~/hpda/lda-test/src/preprocess/distMergeTxtModel.py -mergetxt local global


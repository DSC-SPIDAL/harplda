#!/bin/sh
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

if [ $# -eq "4" ]; then
    clustername=$1
    datasetname=$2
    network_interface=$3
    appname=petuum-$clustername-$datasetname-$network_interface-$4
else
    echo "usage: runpetuum.sh <cluster> <dataset> <ib0|eth0> <appname> "
    exit 
fi

#load config , change the fixed symbol link
#
# cluster_config.$datasetname.$clustername
#

cluster_config=conf/cluster_config
real_config=$cluster_config.$datasetname.$clustername
if [ ! -f $real_config ]; then
    echo "$real_config not exist, quit..."
    exit -1
fi

cd conf && rm -f cluster_config && ln -s cluster_config.$datasetname.$clustername cluster_config && cd ..

. $cluster_config

echo "load $cluster_config ..., ok, cluster=$cluster"
if [ "$cluster" != "$clustername" ] ; then
    echo '$cluster name mismatch, quit ...'
    exit -2
fi

echo "Start runpetuum, load config from $cluster_config as "
echo "work dir = $work"
echo "data set = $datadir"
echo "topics=$topics, iter=$iter, alpha=$alpha, beta=$beta, threads=$threads"

echo "network interface=$network_interface, appname=$appname"

#0. prepare the conf
cd conf
rm $cluster-server.ip $cluster.ip
ln -s $cluster-server-$network_interface.ip $cluster-server.ip
ln -s $cluster-$network_interface.ip $cluster.ip
if [ ! -f $cluster.ip ] ; then
    echo 'make $cluster.ip in conf fail, quit...'
    exit -1
fi
cd ..

#1. clean $workdir
if [ -z $work ] ; then
    echo 'workdir is null, quit...'
    exit -1
fi
echo "start job as $appname"
echo "initialize the working directory"
cexec "mkdir -p $work && cd $work && rm -f * && mkdir -p tmplog"

mkdir -p result
mkdir -p tmplog

# 3. prepare cmd
echo "initialize the machfile..."
#hostfile=$cluster.hostname
machfile=$cluster.mach
id=1
#hosts=(`cat conf/$cluster.hostname`)
#echo $hosts
lasthost=''
#for host in ${hosts[*]}; do


cathosts="cat conf/$cluster.hostname"
hosts=`$cathosts`
echo $hosts

#for host in `cat conf/$cluster.hostname`; do
for host in $hosts; do
    if [ $id -eq '1' ]; then
        ((id++))
        host_list=$host
    else
        host_list=$host_list","$host
    fi
    lasthost=$host
done
host_list=$host_list","$lasthost","$lasthost
echo "host_list as:"$host_list

# add scheduler, and coordinator to the tail

get_last_mach="tail -n 1 conf/$cluster.ip"
last_mach=`$get_last_mach`
cat conf/$cluster.ip >$machfile
echo $last_mach >>$machfile
echo $last_mach >>$machfile
cpush $machfile $work

#cmd="mpirun --hostfile $hostfile --bind-to none ./bin/ldall --machfile $ipfile -threads $threads -num_topic $topics  -num_iter $iter  -data_file $datadir/$datafile -logfile tmplog/1 -wtfile_pre tmplog/wt -dtfile_pre tmplog/dt"
cmd="mpirun -H $host_list --bind-to none $workroot/bin/ldall --machfile $machfile -threads $threads -num_topic $topics  -num_iter $iter  -data_file $datadir/$datafile -logfile learntopics.INFO -wtfile_pre wt -dtfile_pre dt"

#4. run learntopics
echo "Start lda learners......"
date 
cexec monitor.sh start $network_interface

echo $cmd
$cmd 1>>$appname.info.log 2>>$appname.err.log
#$cmd

cexec monitor.sh stop $appname 
date

### 7. prepare for new experiments
echo "Save work directory to work-$appname"
cexec "cd $workroot && mv work work-$appname"

### 8. save the result
mkdir -p result/$appname
cd result/$appname

servercnt="${#hosts[*]}"

server_id=0
for host in ${hosts[*]}; do
    mkdir -p $host
    scp -r $host:$workroot/work-$appname/* $host
   ((server_id++))
done

cd ../..

### 9. collect monitor data
monitor.sh collect $appname
mkdir -p result/$appname/monitorlog
cp -r /mnt/vol1/monitorlog/$appname/* result/$appname/monitorlog

echo "result model files are in result/$appname, enjoy~"







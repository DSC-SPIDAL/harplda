#!/bin/sh
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

if [ $# -eq "6" ]; then
    clustername=$1
    datasetname=$2
    network_interface=$3
    appname=$4
    chkinterval=$5
    reverse_order=$6
else
    echo "usage: runylda.sh <cluster> <dataset> <ib0|eth0> <appname> <chkinterval> <reverse_order>"
    exit 
fi

#load config , change the fixed symbol link
#
# cluster_config.$datasetname.$clustername
#

cluster_config=scripts/cluster_config
real_config=$cluster_config.$datasetname.$clustername
if [ ! -f $real_config ]; then
    echo "$real_config not exist, quit..."
    exit -1
fi

cd scripts && rm -f cluster_config && ln -s cluster_config.$datasetname.$clustername cluster_config && cd ..

. $cluster_config

echo "load $cluster_config ..., ok, cluster=$cluster"
if [ "$cluster" != "$clustername" ] ; then
    echo '$cluster name mismatch, quit ...'
    exit -2
fi

echo "Start ylda, load config from $cluster_config as "
echo "work dir = $work"
echo "data set = $datadir"
echo "topics=$topics, iter=$iter, alpha=$alpha, beta=$beta, threads=$threads"

echo "network interface=$network_interface, chkinterval=$chkinterval, appname=$appname"

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
cexec "mkdir -p $work && cd $work && rm -f * && cp ../input/lda* ."

rm -rf runserver learner global_dict interval_model 
mkdir -p runserver
mkdir -p learner
mkdir -p global_dict
mkdir -p interval_model

mkdir -p result

#2. Clean up
echo "Clean up all DM_server and learners"
cexec "killapp.sh DM_server 2>>/dev/null"
cexec "killapp.sh learntopics 2>>/dev/null"
cexec "cd $bindir && rm * 2>>/dev/null"

#3. DM_Server
echo "Start up the DM_Server......"
cd runserver
sh ../scripts/make_runserver.sh ../conf/$cluster-server.hostname ../conf/$cluster-server.ip
cpush * $bindir
cexec chmod +x $bindir/run_server.'$HOSTNAME'
#cexec /sbin/start-stop-daemon --background --start --exec $bindir/run_server.'$HOSTNAME'
echo "wait for DM_server startup......"
cexec $bindir/run_server.'$HOSTNAME' &

sleep 30
cd ..

#4. run learntopics
echo "Start lda learners......"
cd learner/
cp ../runserver/server.list .
sh ../scripts/make_lda.sh ../conf/$cluster.hostname $chinterval
cpush * $bindir

date 
cexec monitor.sh start $network_interface
cexec sh $bindir/run_lda.'$HOSTNAME'
cexec monitor.sh stop $appname 
date
cd ..

### 5. collect global dict and model
echo "Get global dictionary..."
cd global_dict
sh ../scripts/build_gdict.sh ../conf/$cluster.hostname
cd ..

### 6. close up
echo "Collect all intermediate model files and merge to global model..."
cd interval_model
#sh ../scripts/build_intervalmodel.sh ../conf/$cluster.hostname
sh ../scripts/build_globalmodel.sh $reverse_order $appname
# get logs
cd global
sh ../../scripts/build_logs.sh ../../conf/$cluster.hostname
cd ..

cd ..

echo "Stop DM_Servers ..."
cexec killapp.sh DM_Server

### 7. prepare for new experiments
echo "Save work directory to work-$appname"
cexec "cd $workroot && mv work work-$appname"

### 8. save the result
mkdir -p result/$appname
#cp interval_model/global/* result/$appname
mv interval_model/* result/$appname
cp global_dict/global-dict.wordids result/$appname

### 9. collect monitor data
monitor.sh collect $appname
mkdir -p result/monitorlog
cp -r /mnt/vol1/monitorlog/$appname result/monitorlog

echo "result model files are in result/$appname, enjoy~"







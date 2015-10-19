#!/bin/sh
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

if [ $# -eq "3" -o $# -eq "2" ]; then
    chkinterval=10
    if [ $# -eq "3" ]; then
        chkinterval=$3
    fi
    appname=$2
    cluster_config=$1
else
    echo "usage: runylda.sh <cluster_config> <appname> <chkinterval>"
    exit 
fi

#load config
. $cluster_config


echo "Start ylda, config as "
echo "work dir = $work"
echo "data set = $datadir"
echo "topics=$topics, iter=$iter, alpha=$alpha, beta=$beta, threads=$threads"

#1. distrib train dataset

#1. clean $workdir
if [ -z $work ] ; then
    echo 'workdir is null, quit...'
    exit -1
fi
echo "initialize the working directory"
cexec "mkdir -p $work && cd $work && cp ../input/lda* ."

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


#3. DM_Server
echo "Start up the DM_Server......"
cd runserver
sh ../scripts/make_runserver.sh ../conf/$cluster.hostname ../conf/$cluster.ip
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
cexec monitor.sh start ib0
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
echo "Collect all intermediate model files..."
cd interval_model
sh ../scripts/build_intervalmodel.sh ../conf/$cluster.hostname
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
mv interval_model/ result/$appname
cp global_dict/global-dict.wordids result/$appname

### 9. collect monitor data
monitor.sh collect $appname

echo "result model files are in result/$appname, enjoy~"







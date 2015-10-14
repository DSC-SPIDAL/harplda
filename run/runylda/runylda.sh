#!/bin/sh
if [ $# -eq "3" -o $# -eq "2" ]; then
    chkinterval=100
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

mkdir -p runserver
mkdir -p learner
mkdir -p global_dict
mkdir -p interval_model
mkdir -p result

#3. DM_Server
echo "Start up the DM_Server......"
cd runserver
sh ../scripts/make_runserver.sh ../conf/$cluster.hostname ../conf/$cluster.ip
cpush * $bindir
cexec sh $bindir/killapp.sh DM_server
cexec sh $bindir/run_server.'$HOSTNAME'
cd ..

#4. run learntopics
echo "Start lad learners......"
cd learner/
cp ../runserver/server.list .
sh ../scripts/make_lda.sh ../conf/$cluster.hostname $chinterval
cpush * $bindir
date 
cexec sh $bindir/run_lda.'$HOSTNAME'
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
cd ..

echo "Stop DM_Servers ..."
cexec sh $bindir/killapp.sh DM_Server

### 7. prepare for new experiments
echo "Save work directory to work-$appname"
cexec "cd $workroot && mv work work-$appname"

### 8. save the result
mkdir -p result/$appname
cp interval_model/global/* result/$appname
echo "result model files are in result/$appname, enjoy~"







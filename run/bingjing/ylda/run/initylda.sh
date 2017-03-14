#!/bin/sh
if [ $# -eq "1" ]; then
    cluster_config=$1
else
    echo "usage: initylda.sh <cluster_config> "
    exit 
fi

#load config
. $cluster_config


echo "Start prepare ylda, config as "
echo "work dir = $work"
echo "data set = $datadir"
echo "topics=$topics, iter=$iter, alpha=$alpha, beta=$beta, threads=$threads"

#0. distrib train dataset

#1. clean $workdir
if [ -z $work ] ; then
    echo 'workdir is null, quit...'
    exit -1
fi
cexec "mkdir -p $work && cd $work && rm * 2>>/dev/null"

#2. formatter
mkdir -p formatter

cd formatter
sh ../scripts/make_formatter_new.sh ../conf/$cluster.hostname
cpush * $bindir
#cexec 'sh  "/scratch/pengb/hpda/test/bin/run_formatter."$HOSTNAME'
cexec sh  $bindir/run_formatter.'$HOSTNAME'
cd ..

#3. save to input
cexec "cd $work/.. && mv work input"

#!/bin/sh
if [ $# -eq "2" ]; then
    cluster_config=$1
    rawdatadir=$2
else
    echo "usage: preparedata.sh <cluster_config> <srcdir>"
    echo "       srcdir should be absolute path"
    exit 
fi

#load config
. $cluster_config


echo "Start prepare ylda, config as "
echo "work dir = $work"
echo "data set = $datadir"
echo "topics=$topics, iter=$iter, alpha=$alpha, beta=$beta, threads=$threads"

#0. distrib train dataset
mkdir -p dist
cd dist
~/hpda/lda-test/bin/distrib-seq -make $rawdatadir ../conf/$cluster.hostname
~/hpda/lda-test/bin/distrib-seq -copy $datadir ../conf/$cluster.hostname
cd ..

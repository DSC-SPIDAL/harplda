##!/bin/bash

trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM
. ~/.bashrc

. ~/bin/tbbvars.sh intel64
#homedir=/N/u/fg474admin/hpda/data/
homedir=/scratch/pengb/

use_enwiki()
{
dataset=enwikix
K=100
alpha=1
beta=0.01
timeout=10
}

use_enwiki_big()
{
dataset=enwikix
K=10000
alpha=100
beta=0.01
timeout=50
}



# run_nomad <iternum> <machnumber> <threadnumber> <runid>
run_nomad()
{
    #bin/f+nomad-lda -k 100 -a 100 -b 0.01 -t 10 -n 16 enwiki
    mpirun -f tango-5-ib0.ip -n $2 `pwd`/bin/f+nomad-lda -T $timeout -k $K -a $alpha -b $beta -t $1 -n $3 $homedir/$dataset 2>&1 | tee nomadlda_$1_$2_$3_$dataset-$K-$alpha-$beta_$4.log
}

# run_nx1 $network $runid $dir
run_exp()
{
thread=60
tasks=(5)
for task in ${tasks[*]}; do
    #run_exp $task $thread $2
    run_nomad 100 $task $thread $2
done

#mkdir -p $dataset-30x60-$1-$2
#mv *.log $dataset-30x60-$1-$2

mkdir -p $3
mv *.log $3
}


#==========main===========
network=ib0
#network=eth0

#rm hosts
#ln -s juliet-30-$network.ip hosts

use_enwiki_big
#use_enwiki
#use_yahoomusic

#cexec monitor.sh start $network
runid=$1
appname="$dataset$K-5x60-tango-$network-$runid"
run_exp $network $runid $appname


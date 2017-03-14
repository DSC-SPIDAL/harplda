##!/bin/bash

trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM
. ~/.bashrc

. ~/bin/tbbvars.sh intel64
bin=../bin/
#homedir=/N/u/fg474admin/hpda/data/
homedir=/share/jproject/fg474/dataset/

use_hugewiki()
{
dataset=hugewiki
K=1000
lambda=0.01
eta=0.004
drate=0
reuse=1
timeouts="100 200 400 600 800 1000 1500 2000 3000 4000 5000 6000 8000 10000"
}


# run_nomad <timeout> <machnumber> <threadnumber> <runid>
run_nomad()
{
    mpirun -f juliet-hsw72-30.ip -n $2 `pwd`/nomad_double_0712notrainrmse --timeout $timeouts --dim $K --reg $lambda --lrate $eta --drate $drate --nthreads $3 --path $homedir/$dataset 2>&1 | tee nomad_double_fix_$1_$2_$3_$dataset-$K-$lambda-$eta-$drate_$4.log
}

# run_nx1 $network $runid $dir
run_exp()
{
thread=30
tasks=(30)
for task in ${tasks[*]}; do
    #run_exp $task $thread $2
    run_nomad 10000 $task $thread $2
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

use_hugewiki
#use_yahoomusic

#cexec monitor.sh start $network
runid=$1
appname="$dataset-30x30-hsw72-$network-$runid"
run_exp $network $runid $appname


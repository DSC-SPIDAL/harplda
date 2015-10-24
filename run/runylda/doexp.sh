#!/bin/bash
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

cluster=juliet-30
dataset=enwiki

exp="001"

for expid in $exp; do
    cmd="sh runylda.sh $cluster $dataset ib0 ylda-$dataset-$cluster-ib0.$expid 10 false" 
    echo $cmd
    $cmd | tee ylda-$dataset-$cluster-ib0.$expid.log 

done

cluster=juliet-30
dataset=clueweb

exp="001"

for expid in $exp; do
    cmd="sh runylda.sh $cluster $dataset ib0 ylda-$dataset-$cluster-ib0.$expid 10 false"
    echo $cmd
    $cmd | tee ylda-$dataset-$cluster-ib0.$expid.log 


    cmd="sh runylda.sh $cluster $dataset eth0 ylda-$dataset-$cluster-eth0.$expid 10 false"
    echo $cmd
    $cmd | tee ylda-$dataset-$cluster-eth0.$expid.log 

done




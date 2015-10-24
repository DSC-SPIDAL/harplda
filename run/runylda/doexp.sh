#!/bin/bash
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

cluster=juliet-30
dataset=enwiki

exp="001 002 003"

for expid in $exp; do
    cmd="sh runylda.sh $cluster $dataset ib0 ylda-$dataset-$cluster.$expid 10 false"
    echo $cmd
    $cmd
done




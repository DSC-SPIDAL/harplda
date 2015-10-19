#!/bin/bash
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

exp="1 2 3 "

for expid in $exp; do
    #start monitor
#monitor.sh start ib0    

    #run ylda
    cmd="sh runylda.sh scripts/cluster_config ylda-enwiki-100-$expid 10"
    echo $cmd
    $cmd

    #stop monitor
#    monitor.sh stop ylda-enwiki-100-$expid
#    monitor.sh collect ylda-enwiki-100-$expid

done


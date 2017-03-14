#!/bin/bash
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

#exp="1 2 3 "
exp="0311-2"

for expid in $exp; do
    #run ylda
    cmd="sh runylda.sh scripts/cluster_config ylda-clueweb30b-24-$expid 10"
    echo $cmd
    $cmd | tee ylda-clueweb30b-24-$expid.info.log
done


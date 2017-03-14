#!/bin/bash
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

#exp="1 2 3 "
exp="0313-3"

for expid in $exp; do
    #run ylda
    cmd="sh runylda.sh scripts/cluster_config ylda-enwiki-10-$expid 10"
    echo $cmd
    $cmd | tee ylda-enwiki-10-$expid.info.log
done


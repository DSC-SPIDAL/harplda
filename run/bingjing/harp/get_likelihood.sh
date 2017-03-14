#!/bin/bash

#
# new lda log has likelihood output in the log
#

if [ $# -ne "1" ] ; then
    echo "usage: get_likelihood.sh <logdir>"
    exit -1
fi

for log in `ls $1/container_*000002/syslog`; do
grep -Po "Iteration ([0-9]*), logLikelihood: (.*)" $log | gawk '{print $2,$4}' |sed 's/,//g'
done

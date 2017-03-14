#!/bin/bash
#include the cluster setting
homedir=`dirname $0`


if [ $# -eq "1" -o $# -eq "2" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)

    chkinterval=100
    
    if [ $# -eq "2" ]; then
        chkinterval=$2
    fi
else
    echo "usage: run_petuum.sh <slave file> <chkinterval>"
    exit 
fi



machfile=./mach.vm
rm $machfile
id=1
for host in ${hosts[*]}; do
    ip=`getent hosts $host | awk '{print $1}'`
    echo $ip >>$machfile
    
    if [ $id -eq '1' ]; then
        ((id++))
        host_list=$host
    else
        host_list=$host_list","$host
    fi
done

## mach.vm should be distributed first
#binsrc=/N/u/pengb/hpda/petuum/strads/apps/lda_release/bin/ldall
#
#cpush mach.vm `pwd`
#cpush $binsrc `pwd`/bin
#
#
##run the command
#cmd="mpirun -H $host_list ./bin/ldall --machfile $machfile -threads $threads -num_topic $topics  -num_iter $iter  -data_file $datadir/$datafile -logfile tmplog/1 -wtfile_pre tmplog/wt -dtfile_pre tmplog/dt"
#
#echo $cmd
#
#

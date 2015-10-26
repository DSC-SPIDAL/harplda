#!/bin/bash
#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config

hosts=(`cat slaves`)

#if [ $# -eq "1" -o $# -eq "2" ]; then
#    echo "get server host from $1"
#    hosts=(`cat $1`)
#else
#    echo "usage: run_petuum.sh <slave file> <chkinterval>"
#    exit 
#fi

#topics=10000
#iter=200
#alpha=100
#beta=0.01
#threads=64
if [ -z "${topics+xxx}" ]; then
    echo "topics_num not set yet, quit...."
    exit 
fi

machfile=./mach.vm
rm -f $machfile
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

# mach.vm should be distributed first
#binsrc=/N/u/pengb/hpda/petuum/strads/apps/lda_release/bin/ldall


cexec mkdir -p $work
cexec mkdir -p $work/bin
cexec mkdir -p $work/tmplog
cpush mach.vm $work
echo $ldall
cpush $ldall $work/bin/


#run the command
cmd="mpirun -H $host_list --bind-to none ./bin/ldall --machfile $machfile -threads $threads -num_topic $topics  -num_iter $iter  -data_file $datadir/$datafile -logfile tmplog/1 -wtfile_pre tmplog/wt -dtfile_pre tmplog/dt"

echo $cmd >run.cmd
echo $cmd



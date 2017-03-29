#!/bin/bash
#

help()
{
    echo "analy_harplog.sh <juliet|tango> <appid> <runname> <collectlog>"
}

if [ $# -ne '3' -a $# -ne '4' ]; then
    help
    exit 1
fi

. ~/hpda/lda-test/bin/init_env.sh

#export TESTSET=clueweb-1M

cluster=$1
appid=$2
runname=$3
collectlog=$4

# collect logs
if [ "$cluster" = "tango" ]; then
    # go to t-006
    if [ ! -z $collectlog ]; then
        echo "collect harp log on t-006"
        ssh t-006 "collect_log.sh $appid 2>>/dev/null"
    fi
    echo "get harp log from t-006"
    scp -r t-006:/scratch/hadooplog/$appid /mnt/vol1/hadooplog/
else
    if [ ! -z $collectlog ]; then
        collect_log.sh $appid
    fi
fi


#remove the destination directory first
if [ -d $runname ]; then
    rm -rf $runname
fi
mkdir -p $runname
cd $runname
homedir=`pwd`

# process the log
cp -r /mnt/vol1/hadooplog/$appid $runname
python -m analysis.analy_timelog harp $runname

# get likelihood
#for log in `ls $runname/container_*000002/syslog`; do
#    grep -Po "Iteration ([0-9]*), logLikelihood: (.*)" $log | gawk '{print $2,$4}' |sed 's/,//g' | sed 1d >$runname.likelihood
#done
log=`find $runname -name syslog -exec grep -l -c Iteration {} \; -quit`
if [ -z $log ]; then
    echo "============================================"
    echo "ERROR, no Iteration info found in any syslog"
    echo "============================================"
else
    grep -Po "Iteration ([0-9]*), logLikelihood: (.*)" $log | gawk '{print $2,$4}' |sed 's/,//g' | sed 1d >$runname.likelihood
fi

# copy result
cp $runname.* ../data/opt/

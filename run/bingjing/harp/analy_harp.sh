#
#
#

help()
{
    echo "analy_harp.sh <hdfsdir> <appid> <runname>"
}

if [ $# -ne '3' ]; then
    help
    exit 1
fi

. ~/hpda/lda-test/bin/init_env.sh

#export TESTSET=clueweb-1M

hdfsdir=$1
appid=$2
runname=$3

mkdir -p $runname
cd $runname
homedir=`pwd`

#
#
#
#if [ ! -f $homedir/$runname.likelihood ]; then
#    hadoop fs -copyToLocal $hdfsdir
#    cd `basename $hdfsdir`/model/
#    lda-testp evaluate-harp tmp_model
#    cp tmp_model.likelihood $homedir/$runname.likelihood
#    #delete model
#    rm -rf $hdfsdir
#
#    cd $homedir
#
#else
#    echo "$homedir/$runname.likelihood exists, skip model evaluate"
#fi

#
#
#
#mkdir -p $runname
#collect_log.sh $appid
cp -r /mnt/vol1/hadooplog/$appid $runname
python -m analysis.analy_timelog harp $runname

for log in `ls $runname/container_*000002/syslog`; do
    grep -Po "Iteration ([0-9]*), logLikelihood: (.*)" $log | gawk '{print $2,$4}' |sed 's/,//g' | sed 1d >$runname.likelihood
done

#
#
#
cp $runname.* ../data/opt/

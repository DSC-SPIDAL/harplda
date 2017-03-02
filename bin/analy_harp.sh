#
#
#

help()
{
    echo "analy_harp.sh <hdfsdir> <appid> <runname> <numtopics> <appname>"
}

if [ $# -lt '3' ]; then
    help
    exit 1
fi

if [ -z "$expresultdir" ] ; then
    expresultdir=/tmp/hpda/test/expresult/
fi


hdfsdir=$1
appid=$2
runname=$3
numtopics=$4
appname=$5

mkdir -p $runname
cd $runname
homedir=`pwd`

#
#
#
hadoop fs -copyToLocal $hdfsdir
cd `basename $hdfsdir`/model/
lda-testp evaluate-harp tmp_model $numtopics
cp tmp_model.likelihood $homedir/$runname.likelihood

#
#
#
mkdir -p $runname
cp -r /tmp/hpda/hadooplog/$appid $runname
python -m analysis.analy_timelog harp $runname

#
#
#
cpcmd="cp $runname.* $expresultdir/$appname"
echo $cpcmd
cp $runname.* $expresultdir/$appname


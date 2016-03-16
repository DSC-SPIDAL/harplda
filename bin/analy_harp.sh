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

hdfsdir=$1
appid=$2
runname=$3

mkdir -p $runname
cd $runname
homedir=`pwd`

#
#
#
hadoop fs -copyToLocal $hdfsdir
cd `basename $hdfsdir`/model/
lda-testp evaluate-harp tmp_model
cp tmp_model.likelihood $homedir/$runname.likelihood

#
#
#
mkdir -p $runname
cp -r /mnt/vol1/hadooplog/$appid $runname
python -m analysis.analy_timelog harp $runname

#
#
#
cp $runname.* ../data/newharp/

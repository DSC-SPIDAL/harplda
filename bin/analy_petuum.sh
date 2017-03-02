#!/bin/bash
#
#

help()
{
    echo "analy_petuum.sh <dir> <appname>"
}

if [ $# -ne '2' ]; then
    help
    exit 1
fi

if [ -z "$expresultdir" ] ; then
    expresultdir=/tmp/hpda/test/expresult/
fi


appdir=$1
appname=$2

#
#
#
python -m analysis.analy_timelog petuum-run $appdir
python -m analysis.analy_timelog petuum $appdir


#
#
#
if [ ! -d $expresultdir$appname ] ; then
    mkdir -p  $expresultdir$appname 
fi

cpcmd="cp $appdir.* $expresultdir/$appname"
echo $cpcmd
cp $appdir.* $expresultdir/$appname


#!/bin/sh

#
# remove top K lines, and draw the likelihood plot
#

if [ $1 -eq '-h' ]; then
    echo "usage: draw_tail.sh <remove topK> <figname>"
    echo "   topK = 5, figname=lda by default"
    exit 0
fi

topK=$1
figname=$2
if [ -z $figname ] ; then
    figname=lda
fi

if [ -z $topK ] ; then
    topK="5"
fi

mkdir -p tail

for f in `ls *.likelihood`; do
    cmd="sed -e 1,"$topK"d $f"
    echo $cmd
    $cmd >tail/$f
done

cd tail
python ~/hpda/lda-test/src/evaluation/test_likelihood.py -draw $figname-tail




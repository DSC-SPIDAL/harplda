#!/bin/bash

help()
{
    echo "usage: build_petsc.sh <mrlda file> <data name>"
    exit -1
}

if [ $# -ne "2" ] ; then
    help
fi

mrlda=$1
dataname=$2

# split
mkdir -p split
cd split
#split -l 10000 -a 4 $mrlda
#python ~/hpda/mf-test/src/preprocess/mrlda.py "xa*" $dataname
#head -10 "$dataname"-x.mm >test.mm
#python ~/hpda/mf-test/src/preprocess/mm2nomad.py -big "$dataname"-x.mm test.mm .

#make meta
line=`head -2 "$dataname"-x.mm |tail -1`
nnz=`wc -l "$dataname"-x.mm | tail -1 | gawk '{print $1}'`
nnz=`echo "$nnz - 2" | bc`
cd ..
echo $line | gawk '{print $2}' > meta
trainmsg=`echo $line | gawk '{print $1}'`
echo "$trainmsg $nnz $nnz $dataname"".train.petsc" >> meta
echo "0 0 0 $dataname"".test.petsc" >> meta

#copy test petsc
cp /share/jproject/fg474/dataset/enwikix/enwiki-1M-x.mm.test.petsc "$dataname".test.petsc
cp split/train.dat "$dataname".train.petsc

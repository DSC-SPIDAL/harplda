#!/bin/sh

if [ $# -ne '1' ] ; then
    echo 'usage: make_testset.sh <testset name>'
    exit -1
fi

testset=$1
if [ ! -f $testset.mrlda.txt ]; then
    echo '$testset.mrlda.txt not found, quit'
    exit -2
fi

#tail -200000 pubmed.mrlda.reid.txt >pubmed-test-200k.mrlda.txt


python ~/hpda/lda-test/src/datastat/docStat.py $testset.mrlda.txt
python ~/hpda/lda-test/src/preprocess/mrlda2ylda.py $testset.mrlda.txt

for f in `ls *.ylda`; do echo $f && ~/hpda/lda-test/tool/mallet/bin/mallet import-file --input $f --output `basename $f .ylda`.mallet --keep-sequence --token-regex "[\p{L}\p{N}_]+|[\p{P}]+"; done


~/hpda/lda-test/tool/mallet/bin/mallet evaluate-topics --dumpAlphabet all.dict --input $testset.mrlda.txt.mallet
mv all.dict.data $testset.mallet.dict

mv $testset.mrlda.txt.mallet $testset.mallet.txt

#clean up
rm all.dict*
rm *.pickle
rm *.ylda
rm *.doc
rm $testset.mrlda.txt.dict

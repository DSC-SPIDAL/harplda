if [ ! -f $1.mallet ] ; then
    python ~/hpda/lda-test/src/preprocess/convertTxt2Mallet.py $1 x x False
fi

~/hpda/lda-test/tool/mallet/bin/mallet evaluate-topics --printModel ok --modeldata $1.mallet --input x

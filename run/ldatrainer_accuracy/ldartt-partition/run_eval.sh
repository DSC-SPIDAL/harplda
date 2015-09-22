curdir=`pwd`
export TESTSET=pubmed

#harp output directory, $d/model/tmp_model
for d in `ls`; do
echo $d
if [ -d $d ]; then
    echo "do on $d"
    cd $d/model
    lda-testp evaluate-harp tmp_model
    cp tmp_model.likelihood $curdir/$d.likelihood
    cd $curdir
fi

done


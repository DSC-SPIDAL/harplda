curdir=`pwd`
export TESTSET=enwiki-1M
export jobsthreads=8

#harp output directory, $d/model/tmp_model
for d in `ls`; do
echo $d
if [ -d $d ]; then
    echo "do on $d"
    cd $d/model
    lda-testmodel evaluate-harp tmp_model
    cd $curdir
fi

done

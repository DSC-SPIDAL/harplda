curdir=`pwd`
export TESTSET=enwiki-1M
export jobsthreads=8

#harp output directory, $d/model/tmp_model
for d in `ls`; do
echo $d
if [ -d $d ]; then
    echo "do on $d"
    cd $d
    lda-testmodel evaluate-harp global
    cd $curdir
fi

done

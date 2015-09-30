workdir=/scratch/pengb/hpda/test/clueweb/

out1=$workdir/out1
mkdir -p $out1

cd $workdir/mrlda

for d in `ls`; do 
    if [ -d $d ] ; then 
        python ~/hpda/lda-test/src/corpus/webcorpus.py -mergefreq $d $out1/$d.all
    fi
done

out2=$workdir/out2
mkdir -p $out2

cd $workdir/out1

python ~/hpda/lda-test/src/corpus/webcorpus.py -mergefreq . $out2/$HOSTNAME

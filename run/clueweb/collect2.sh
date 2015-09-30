workdir=/scratch/pengb/hpda/test/clueweb/

out2=$workdir/out2
mkdir -p $out2

cd $workdir

python ~/hpda/lda-test/src/corpus/webcorpus.py -mergefreq out0 $out2/$HOSTNAME

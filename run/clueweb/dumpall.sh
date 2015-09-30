workdir=/scratch/pengb/hpda/test/clueweb/
out2=$workdir/out2
mkdir -p $out2

cd $workdir/out0

for d in `ls *.all.freq`; do
    fname=`basename $d .freq`
    python ~/hpda/lda-test/src/corpus/webcorpus.py -dump $fname
    head -2000000 $fname.txt.freq >>../out2/_all.txt.freq
done

sort ../out2/_all.txt.freq > ../out2/all.txt.freq

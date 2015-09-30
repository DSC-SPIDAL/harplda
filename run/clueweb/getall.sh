. ~/.bashrc

workdir=/scratch/pengb/hpda/test/clueweb/

indir=$workdir/sortedid-1M
outdir=$workdir/clueweb
mkdir -p $outdir

cd $indir

input=`find . -name "*.gz.mrlda"`
for f in $input; do
    bname=`basename $f`
    dirname=`dirname $f`
    dirname=`basename $dirname`
    ln -s $indir/$f $outdir/$dirname-$bname
done


. ~/.bashrc

workdir=/mnt/vol1/pengb/hpda/test/noreid

inputdir=clueweb-input
outdir=clueweb-noreid
mkdir -p $outdir

dictfile=new.id

input=`ls $inputdir/`
inputlist=""
outputlist=""
for f in $input; do
    dirname=`dirname $f`
    dirname=`basename $dirname`
    basename=`basename $f`
    inputlist=$inputlist" $inputdir/"$f
    outputlist=$outputlist" $outdir/"$basename
done

do_convert(){
    #input.mrlda new.id output.mrlda
    python /N/u/pengb/hpda/lda-test/src/preprocess/mrlda2id.py $1 $2 $3
}

export -f do_convert 

cmd="parallel --xapply --jobs 32 do_convert ::: $inputlist ::: $dictfile ::: $outputlist"
echo $cmd
$cmd





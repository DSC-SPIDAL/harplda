. ~/.bashrc

workdir=/scratch/pengb/hpda/test/clueweb/

outdir=$workdir/sortedid-1M
mkdir -p $outdir

cd $workdir/mrlda
dictfile=../sortedid-1M.newid

input=`find . -name "*.gz.mrlda"`
inputlist=""
outputlist=""
for f in $input; do
    dirname=`dirname $f`
    dirname=`basename $dirname`
    mkdir -p ../sortedid-1M/$dirname
    inputlist=$inputlist" "$f
    outputlist=$outputlist" ../sortedid-1M/"$f
done

do_convert(){
    #22.warc.gz.mrlda ../sortedid-1M.newid 22.reid
    python /N/u/pengb/hpda/lda-test/src/corpus/webcorpus.py -convertid $1 $2 $3
}
#22.warc.gz.mrlda ../sortedid-1M.newid 22.reid

#for d in `ls`; do 
#    if [ -d $d ] ; then 
#        python ~/hpda/lda-test/src/corpus/webcorpus.py -mergefreq $d $out1/$d.all
#    fi
#done

export -f do_convert 

cmd="parallel --xapply --jobs 4 do_convert ::: $inputlist ::: $dictfile ::: $outputlist"
echo $cmd
$cmd





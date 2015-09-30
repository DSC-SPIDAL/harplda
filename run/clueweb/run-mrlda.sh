trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM
unset PYTHONHOME
unset PYTHONPATH
. /N/u/pengb/.bashrc

workdir=/scratch/pengb/hpda/test/clueweb
outdir=$workdir/mrlda2

cd $workdir

#create outdir
dirs=`find -L data -type d -name "en*"`
for d in $dirs; do
    dir=`basename $d`
    echo "mkdir -p $outdir/$dir"
    mkdir -p $outdir/$dir
done

#prepare parameters
inputlist=`find -L data -name "*.tw"`
outputlist=""
for f in $inputlist; do
    dir=`dirname $f`
    dirp=`basename $dir`
    basename=`basename $f .tw`
    outputlist=$outputlist" mrlda2/"$dirp/$basename".mrlda"
done

do_convert(){
    echo $1, $2
    if [ -f $2 ] ; then
        echo "$2 exists already, happy go to next one"
    else
        /N/u/pengb/hpda/lda-test/third_party/twreader/twreader $1 > $2.input
        python /N/u/pengb/hpda/lda-test/src/corpus/webcorpus.py -make $2.input $2
        rm $2.input
    fi
}


export -f do_convert 
cmd="/N/u/pengb/bin/parallel --xapply --jobs 8 do_convert ::: $inputlist ::: $outputlist"
echo $cmd
$cmd




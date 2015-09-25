unset PYTHONHOME
unset PYTHONPATH
. /N/u/pengb/.bashrc

workdir=/scratch/pengb/hpda/test/clueweb
outdir=$workdir/mrlda

inputs=`find $workdir/data -name "*.input"`
mkdir -p $outdir

outputs=""
for f in $inputs; do
    basename=`basename $f .input`
    outputs=$outputs" mrlda/"$basename".mrlda"
done

do_convert(){
    python /N/u/pengb/hpda/lda-test/src/corpus/webcorpus.py -make $1 $2
}

cd $workdir

export -f do_convert 
cmd="/N/u/pengb/bin/parallel --xapply --jobs 8 do_convert ::: $inputs ::: $outputs"
echo $cmd
$cmd



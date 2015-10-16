outdir=$1
mkdir -p $outdir

for d in `ls`; do 
    if [ -d $d ]; then
        cp $d/model/tmp_model.likelihood $outdir/$d.likelihood
    fi
done

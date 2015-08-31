echo "run experiments with ylda"

curdir=`pwd
cd /scratch/pengb/ylda && source /scratch/pengb/ylda/setLibVars.sh
cd $curdir
mkdir -p ylda
cd ylda

for f in `ls ../pubmed-*.ylda`; do 
    echo $f
    dname=`basename $f .mrlda.txt.ylda`
    mkdir $dname
    cd $dname
    cat ../$f | /scratch/pengb/ylda/formatter

    #learn
    #python ../learn.py

    cd ..
done

cd $curdir

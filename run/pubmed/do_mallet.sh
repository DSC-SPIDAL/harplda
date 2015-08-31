prefix=pubmed-
suffix=mrlda.txt

echo "run experiments with mallet"

curdir=`pwd`
mkdir -p mallet
cd mallet

for f in `ls ../pubmed-*.mallet`; do 
    echo $f
    dname=`basename $f .mrlda.txt.mallet`
    mkdir $dname
    cd $dname

    input=../$f
    #learn
    #python ../learn.py
    python ../learn.py " ~/hpda/lda-test/tool/mallet/bin/mallet train-topics --input $input --num-topics 2000 --num-iterations 1000 --inferencer-filename infer --evaluator-filename evaluator --alpha 20 --beta 0.01 --use-symmetric-alpha true"
    #python learn.py " ~/hpda/lda-test/tool/mallet/bin/mallet train-topics --input $1 --num-topics 2000 --num-iterations 1000 --inferencer-filename infer --evaluator-filename evaluator --num-threads 8  --alpha 20 --beta 0.01 --use-symmetric-alpha true"

    cd ..
done

cd $curdir

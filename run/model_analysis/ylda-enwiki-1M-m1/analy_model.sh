
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

workdir=
klist=`echo "100 1000 3000 10000 20000"`

for k in $klist; do

for f in `ls *.hyper`; do
    basename=`basename $f .hyper`
    echo $basename
    python ~/hpda/lda-test/src/analysis/analy_modeldata.py -txt $basename dict.wordids $k
done

done

python ~/hpda/lda-test/src/analysis/plot.py config cdf-modelsize.png . "K-.*"


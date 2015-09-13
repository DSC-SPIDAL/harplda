home=/scratch/pengb/hpda/test/
ylda=/scratch/pengb/ylda

cd $ylda
source setLibVars.sh

workdir=$home/work
mkdir $workdir
cd $workdir

ln -s $ylda/Tokenizer.class Tokenizer.class

for f in `ls ../ap`; do
    cat ../ap/$f | java Tokenizer | $ylda/formatter
done



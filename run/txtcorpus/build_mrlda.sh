
if [ $# -ne "3" ]; then
    echo "Usage: build_mrlda.sh <txtcorpus> <cut-off word cnt> <vocabsize>"
    exit 0
fi

txtcorpus=$1
start=$2
vocabsize=$3
head=`echo "$vocabsize+$start" | bc`

echo 'build mrlda from '$txtcorpus.txt' , head='$head' vocabsize='$vocabsize

awk 'BEGIN{print 1000}{print $2,$1}' $txtcorpus.txt.dict>wordmap
python ~/hpda/lda-test/src/preprocess/wordmap2wordids.py wordmap $txtcorpus.txt.freq wordid
sort -nr -k 3 wordid >wordid.sort
head -$head wordid.sort | tail -n $vocabsize >newdict
awk 'BEGIN{print 0;cnt=10}{print $1,cnt; cnt +=1}' newdict >new.wordmap
python ~/hpda/lda-test/src/preprocess/mrlda2id.py $txtcorpus.txt new.wordmap $txtcorpus.mrlda

. ~/hpda/lda-test/bin/init_env.sh

mkdir -p out-short out-full
rm out-short/* out-full/* *.pdf

if [ $# -eq "0" ]; then
    confdir=ldaopt
else
    confdir=$1
fi

#
# short view
#
#for conf in `ls $confdir/*.conf`; do
#    python plotldaopt.py $conf TRUE 20000
#done
#for conf in `ls $confdir/*scale.conf`; do
#    python plotldascale.py $conf TRUE 20000
#done
#
#mv $confdir/*.pdf out-short

#
# full view
#
#for conf in `ls $confdir/*.conf`; do
#    python plotldaopt.py $conf 
#done
for conf in `ls $confdir/*scale.conf`; do
    python plotldascale.py $conf 
done


mv $confdir/*.pdf out-full

mkdir -p ~/tmp/runsocc/$confdir
cp -r out-full/* ~/tmp/runsocc/$confdir

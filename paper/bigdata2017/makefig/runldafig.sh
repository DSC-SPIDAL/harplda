. ~/hpda/lda-test/bin/init_env.sh

mkdir -p out-full
rm out-full/* 

if [ $# -eq "0" ]; then
    confdir=ldaopt
else
    confdir=$1
fi

#
# full view
#
for conf in `ls $confdir/*.conf`; do
    python plotldaall.py $conf 
done

mv $confdir/*.pdf out-full

mkdir -p ~/tmp/runsocc
mkdir -p ~/tmp/runsocc/$confdir
rm ~/tmp/runsocc/$confdir/*

cp -r out-full/* ~/tmp/runsocc/$confdir

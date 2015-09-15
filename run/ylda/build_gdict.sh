ylda=/scratch/pengb/ylda
work=/scratch/pengb/hpda/test/work

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo 'get server host from slaves'
    hosts=(`cat slaves`)
fi

topics=1000
iter=1000
servercnt="${#hosts[*]}"

echo 'get all lda.dict.dump from clients'
server_id=0
for host in ${hosts[*]}; do
    scp $host:$work/lda.dict.dump lda.dict.dump.$server_id
   ((server_id++))
done

echo "run Merge_Dictionaries"
curdir=`pwd`
cd $ylda && source $ylda/setLibVars.sh
cd $curdir
echo "$ylda/Merge_Dictionaries --dictionaries=$servercnt --dumpprefix=lda.dict.dump"
$ylda/Merge_Dictionaries --dictionaries=$servercnt --dumpprefix=lda.dict.dump

echo 'distribute lda.dict.dump.global'
for host in ${hosts[*]}; do
    scp lda.dict.dump  $host:$work/lda.dict.dump.global
done



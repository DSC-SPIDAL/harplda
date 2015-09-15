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

echo 'get all global_model from clients'
server_id=0
file='global_model'
for host in ${hosts[*]}; do
    scp $host:$work/$file $file.$server_id
    scp $host:$work/$file.hyper $file.hyper.$server_id
    cat $file.$server_id >> $file
   ((server_id++))
done





ylda=/scratch/pengb/ylda
work=/scratch/pengb/hpda/test/result

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo 'get server host from slaves'
    hosts=(`cat slaves`)
fi

topics=20
iter=1000

server_list=`cat server.list`
server_id=1

for host in ${hosts[*]}; do
    echo "echo \"run Merge_Topic_Counts on madrid-00$server_id\"" >  run_merger.madrid-00$server_id
    echo "cd $ylda && source $ylda/setLibVars.sh" >> run_merger.madrid-00$server_id
    cmd="cd $work && nohup $ylda/Merge_Topic_Counts --topics=$topics --clientid=$server_index --servers=$server_list --globaldictionary="lda.dict.dump.global" &"
    echo $cmd >> run_merger.madrid-00$server_id
    ((server_id++))
done



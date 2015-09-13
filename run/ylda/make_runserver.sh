ylda=/scratch/pengb/ylda
work=/scratch/pengb/hpda/test/server

if [ $# -eq "1" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)
else
    echo 'get server host from slaves'
    hosts=(`cat slaves`)
fi

num_servers=${#hosts[*]}
num_clients=$num_servers
port=10000
model=1

server_id=1
server_list=""
for host in ${hosts[*]}; do
    echo "echo \"run DM_Server on madrid-00$server_id\"" >  run_server.madrid-00$server_id
    echo "cd $ylda && source $ylda/setLibVars.sh" >> run_server.madrid-00$server_id

    ((server_index=server_id-1))
    cmd="cd $work && nohup $ylda/DM_Server $model $server_index $num_clients $host:$port --Ice.ThreadPool.Server.SizeMax=9 &"
    echo $cmd >> run_server.madrid-00$server_id

    if [ "$server_id" -ne "1" ] ; then
        server_list=$server_list,$host:$port
    else
        server_list=$host:$port
    fi

    ((server_id++))
done

echo $server_list >server.list

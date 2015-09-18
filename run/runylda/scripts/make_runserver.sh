#include the cluster setting
homedir=`dirname $0`
. $homedir/cluster_config

if [ $# -eq "2" ]; then
    echo "get server host from $1"
    hosts=(`cat $1`)

	echo "get server ip list from $2"
	iplist=(`cat $2`)

else
    echo "usage: make_runserver.sh <hostname file> <ipname file>"
    exit 
fi

echo ${iplist[*]}

num_servers=${#hosts[*]}
num_clients=$num_servers
port=10000
model=1

server_id=1
server_list=""
for host in ${hosts[*]}; do
    echo "echo \"run DM_Server on $host\"" >  run_server.$host
    echo "cd $ylda && source $ylda/setLibVars.sh" >> run_server.$host

    ((server_index=server_id-1))
    hostip=${iplist[$server_index]}

    #cmd="cd $work && nohup $ylda/DM_Server $model $server_index $num_clients $hostip:$port --Ice.ThreadPool.Server.SizeMax=9 &"
    cmd="cd $work && $ylda/DM_Server $model $server_index $num_clients $hostip:$port --Ice.ThreadPool.Server.SizeMax=$num_servers "
    echo $cmd >> run_server.$host

    if [ "$server_id" -ne "1" ] ; then
        server_list=$server_list,$hostip:$port
    else
        server_list=$hostip:$port
    fi

    ((server_id++))
done

echo $server_list >server.list

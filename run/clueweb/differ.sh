
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM
outdir=/scratch/pengb/hpda/test/clueweb/data
#input="en0089 en0087 en0092 en0093 en0090 en0085 en0086"
#serverlist="m1 m2 m3 m4 m5 m6 m8"
input="en0087 en0092 en0093 en0090 en0085 en0086"
serverlist="m2 m3 m4 m5 m6 m8"
server=(`echo $serverlist`)

do_scp(){
    cmd="scp -r $1 $2:$3"
    $cmd
}

export -f do_scp 

cmd="parallel --xapply --jobs 3 do_scp ::: $input ::: $serverlist ::: $outdir"
echo $cmd
$cmd



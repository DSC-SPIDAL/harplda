trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

do_twread(){
    ./twreader $1 > $2
}

dirs=`find /scratch/pengb/data -type d -name "en*"`
echo $dirs

output=raw

for d in $dirs; do
    dir=`basename $d`
    #echo $dir
    #mkdir -p $dir
    mkdir -p $output/$d
done

inputlist=`find /scratch/pengb/data -name "*.tw"`
outputlist=""
for f in $inputlist; do
    outputlist=$outputlist" "$output/$f.input
done

export -f do_twread

cmd="parallel --xapply --jobs 12 do_twread ::: $inputlist ::: $outputlist"
echo $cmd
$cmd



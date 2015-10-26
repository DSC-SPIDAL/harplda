if [ $# -eq '2' ]; then
    workdir=$1
    reverse_order=$2
else
    echo "useage: getmodel.sh <work homedir> <reverse_order>"
    exit 0
fi

echo 'reverse order = ', $reverse_order

for d in `cat worklist`; do
    mkdir -p $d
    echo "enter $d"
    cd $d
    sh $workdir/scripts/build_globalmodel.sh $reverse_order $d
    cd ..
done


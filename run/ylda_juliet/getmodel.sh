for d in `cat worklist`; do
    echo "enter $d"
    cd $d
    sh build_globalmodel.sh juliet-100.hostname $d
    cd ..
done


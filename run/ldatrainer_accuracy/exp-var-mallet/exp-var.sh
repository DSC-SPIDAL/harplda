#variance test for mallet
todolist="1 2 3"
trainset="`pwd`/../pubmed-2M.mallet.txt"
export TESTSET=pubmed

echo "trainset=", $trainset
for f in $todolist; do
    mkdir $f
    cd $f
    date
    sh ../run_mallet.sh $trainset
    date
    cd ..

done

#run lda-test
for f in $todolist; do
    lda-testp evaluate-mallet $f
done

#run lda-test, because the final .likelihood file was not created
for f in $todolist; do
    lda-test evaluate-mallet $f
done



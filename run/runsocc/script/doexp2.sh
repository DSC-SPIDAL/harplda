threads=(1 2 4 8 16)
datasets=("nytimes" "pubmed2m")

#
#for dataset in ${datasets[*]}; do
#for thread in ${threads[*]}; do
#    #runlightlda.sh <dataset> <iters> <topics> <nodes> <threads> <mf_steps> <runid>
#    sh runlightlda-new.sh $dataset 200 1000 1 $thread 2 0327A
#done
#done

#
for dataset in ${datasets[*]}; do
for thread in ${threads[*]}; do
    #runlightlda.sh <dataset> <iters> <topics> <nodes> <threads> <mf_steps> <runid>
    sh runwarplda.sh $dataset 200 1000 1 $thread 2 0327A
done
done


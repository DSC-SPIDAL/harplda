#confs=("2x4_" "2x16_" "4x4_" "4x16_" "8x4_" "8x16_")
confs=(2x16 4x16 8x16)

for pat in ${confs[*]}; do
grep "$pat"_ list.txt | sed '/straggler/d'  > enwiki_distributed_"$pat".conf
grep "$pat"_ list.txt | sed '/nomad/d' | sed '/straggler/d' > enwiki_distributed_"$pat"_cv.conf
done

grep "x16_" list.txt | sed '/straggler/d' > enwiki_distributed_x16_scale.conf

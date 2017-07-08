#confs=("2x4_" "2x16_" "4x4_" "4x16_" "8x4_" "8x16_")
confs=(2x16 4x16 8x16)

for pat in ${confs[*]}; do
grep "$pat"_ list.txt | sed '/straggler/d'  > testexp_"$pat".conf
done

grep "x16_" list.txt | sed '/straggler/d' > testexp_x16_scale.conf

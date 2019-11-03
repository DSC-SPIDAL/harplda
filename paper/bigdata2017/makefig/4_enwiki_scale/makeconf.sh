#confs=("2x4_" "2x16_" "4x4_" "4x16_" "8x4_" "8x16_")
confs=(10 20 30)

for pat in ${confs[*]}; do
grep " $pat" list.txt > enwikiscale_"$pat".conf
done

cp list.txt enwikiscale_scale.conf

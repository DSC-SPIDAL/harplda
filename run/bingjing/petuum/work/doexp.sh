#!/bin/sh
trap "echo 'signal.....quit'; exit" SIGHUP SIGINT SIGTERM

#sh runpetuum.sh juliet-30 clueweb30b ib0 harp3_clueweb30_ipdps_30x20_D001
#sh runpetuum.sh juliet-45 clueweb30b ib0 harp3_clueweb30_ipdps_45x20_D001
#sh runpetuum.sh juliet-60 clueweb30b ib0 harp3_clueweb30_ipdps_60x20_A003
#sh runpetuum.sh juliet-30 clueweb30b ib0 harp3_clueweb30_ipdps_30x20_A002
#sh runpetuum.sh juliet-60 clueweb30b ib0 harp3_clueweb30_ipdps_60x20_A002

#sh runpetuum.sh juliet-30 clueweb30b ib0 harp3_clueweb30_ipdps_30x20_hsw72_A001

sh runpetuum.sh juliet-10 enwiki-1M ib0 harp3_enwiki_ipdps_10x30_hsw72_A001

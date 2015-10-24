Run YahooLDA
===========================

1. prepare the cluster_config files under scripts and conf

2. compile the latest code under tool/ylda, and install bins to $ylda directory

```sh

diff -rq src/ ~/hpda/lda-test/tool/ylda/Yahoo_LDA/src/ |grep diff | awk '{print "cp ",$2,$4}' >update.sh
sh update.sh

sh scripts/install_ylda.sh
```

3. run it

```sh

sh preparedata.sh scripts/cluster_config `pwd`/../noreid/enwiki-noreid
sh initylda.sh scripts/cluster_config
#"usage: runylda.sh <cluster> <dataset> <ib0|eth0> <appname> <chkinterval> <reverse_order>"
sh runylda.sh  juliet-30 enwiki ib0 ylda.enwiki.juliet-30.demo 10 false
```

the final model files are under result/ylda.enwiki.juliet-30.demo

refer to doexp.sh

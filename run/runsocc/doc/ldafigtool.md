lda figs tool
===============

workdir:  juliet-128:/tmp/hpda/pengb/hpda/test/bingjing/harp

###1. analysis harp log

```sh
analy_harplog.sh <juliet|tango> <appid> <runname> <collectlog>
     juliet|tango     ; which cluster the logs come from
     appid          ; harp job appid
     runname     ;  the name used for fig drawing
     collectlog     ; if exists, then do collect_log before analysis
```

example:

```sh
     cd /tmp/hpda/pengb/hpda/test/bingjing/harp
     ./analy_harplog.sh juliet application_1490647726864_0011 \
         harp_clueweb30b_24x30_juliet_timer_50-60_0011 collect
```

refer to gettimertuning.sh for more

###2. view the result data
result data dir: /tmp/hpda/pengb/hpda/test/bingjing/harp/data/opt

example:

```sh
     cd /tmp/hpda/pengb/hpda/test/bingjing/harp/data/opt
     cat harp_clueweb30b_24x30_juliet_timer_50-60_0011.likelihood
```

###3. draw figs
makefig workdir: /tmp/hpda/pengb/hpda/test/bingjing/harp/test/makefig

create the configure file, refer to the configure files under the directory 'timetuning'
then run 'runldafig.sh \<confdir\>' to make the figs

example:

```sh
     cd /tmp/hpda/pengb/hpda/test/bingjing/harp/test/makefig
     sh runldafig.sh timetuning
```

finally, all the figs made will appear in ~/tmp/bingjing/\<confdir\>, which is ~/tmp/bingjing/timetuning in this case

###4. copy figs from j-128 to local disk
the script scopy.sh can help, which located at ~/bin/scopy.sh on j-128

run the following command, it will copy all files in j-128:~/tmp/bingjing/timetuning to current directory:

```sh
     scopy.sh fg474admin "bingjing/timetuning"
```

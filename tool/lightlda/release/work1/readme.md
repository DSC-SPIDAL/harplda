work1
========

This version works fine for multithreading and even with mpi.
stop_watch class rewrote.
the Log output changed to support analysis, add rankid.

issue: the "training time use" only output the first thread value, 
it's more than unbalanced.

todo: change to sync each iteration, anyway, only count the training time
that's fair.

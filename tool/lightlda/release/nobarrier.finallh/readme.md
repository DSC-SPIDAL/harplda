nobarrier.finallh
========

this version exclude the Barrier Fix in 'barrier' version
and only output the likelihood at the end of all iterations
in order to check the asynachronous performance of lightlda


----barrier----
This version works on top of work1
fix issue: the "training time use" only output the first thread value, 
it's more than unbalanced.

commit: 
add barrier for all the threads in each iteration, anyway, only count the training time that's fair.
remove doc likelihood caculation


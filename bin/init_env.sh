#
# set the source code path
# SRCHOME
#

#export env setting
export _INSTDIR_=$HOME/hpda/lda-test/
echo 'Set _INSTDIR_ ->', $_INSTDIR_

#add to PYTHONPATH
if [ ! $_OLD_PYTHONPATH ] ; then
    export _OLD_PYTHONPATH=$PYTHONPATH
fi
export PYTHONPATH=$_INSTDIR_/src:$_OLD_PYTHONPATH


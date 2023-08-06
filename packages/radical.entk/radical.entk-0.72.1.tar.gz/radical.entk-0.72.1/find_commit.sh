#!/bin/sh

cfile=$1

test -z "$cfile" && echo "need commit file"
test -z "$cfile" && exit 1

# ------------------------------------------------------------------------------
#
progress(){

  while read X
  do
    echo -n .
  done
  echo
}

max=$(wc -l $cfile | cut -f 1 -d ' ')
n=$max
commits=$(tac $cfile)
while true
do
    c=$(cat $cfile | head -n $n | tail -n 1)
    printf "\n==============================\n%3d / %3d: $c  " $n $max
    read X

    if test "$X" = "s"
    then
        n=$((n-1))

    elif test "$X" = "b"
    then
        n=$((n+1))

    elif test -z "$X"
    then
        echo -n 'git co  : '
        git checkout $c  2>&1 | progress
        echo -n 'install : '
        make reinstall   2>&1 | progress
        echo -n 'run     : '
        stdbuf -oL ./test_issue_26.py 2>&1 | tee r.x.out | progress
        echo -n 'exit    : $?'

    else
        n=$X
    fi

done

